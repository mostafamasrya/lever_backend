from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from rest_framework.generics import CreateAPIView,UpdateAPIView,DestroyAPIView,RetrieveAPIView
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.shortcuts import render, redirect
from lever.users.models import User
import pandas as pd
from django.db.models import Sum, Avg, Count, Q
from django.http import HttpResponse
from django.utils.timezone import is_aware, timezone
from .models import Company, Client
from django import forms
from lever.users.serializers import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse









from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView,RetrieveUpdateAPIView
import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
import os
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.http import StreamingHttpResponse, HttpResponseBadRequest
from botocore.client import Config
from .serializers import *  

def default_success_response(data=[],status_code=200,message="success",error_code=1000):
    return {
        "status": "success",
        "status_code": status_code,
        "error_code": error_code,

        "message": message,
        "data": data,
    }

def default_error_response(data=[],status_code=400,message="error",error_code=1000):
    return {
        "status": "error",
        "status_code": status_code,
        "error_code": error_code,
        "message": message,
        "data": data,
    }      


def check_required_fileds(required_fields,data):
    for field in required_fields:
        if field not in data or not data[field]:
            msg = _("required")
            message = _(field) + " " + msg
            # message = {"message":message}
            return message
    return ""







class UploadExcelFileForm(forms.Form):
    file = forms.FileField()



class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None=None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()




def export_clients_excel(request, company_id):
    """Generate and serve Excel file for clients of a selected company."""
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return HttpResponse("Company not found", status=404)

    # Fetch clients for the selected company
    clients = Client.objects.filter(compnay=company)

    # Prepare data for export
    data = []
    for client in clients:
        created_at = client.created_at
        if is_aware(created_at):
            created_at = created_at.astimezone(timezone.utc).replace(tzinfo=None)

        data.append({
            'name': client.name,
            'national_id': client.national_id,
            'email': client.email,
            'phone_number': client.phone_number,
            'paid_money': client.paid_money,
            'money_left': client.money_left,
            'created_at': created_at,
        })

    # Create a DataFrame using pandas
    df = pd.DataFrame(data)

    # Create an Excel file in memory
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{company.name}_clients.xlsx"'

    # Use pandas to write the DataFrame to an Excel file
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response




def upload_clients_view(request):
    if request.method == 'POST':
        form = UploadExcelFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']  # Get the uploaded file
            try:
                # Read the Excel file using pandas
                df = pd.read_excel(file)

                # Define required columns
                required_columns = ['name', 'email', 'national_id', 'phone_number', 'paid_money', 'money_left']

                # Check if the Excel file contains the required columns
                if not all(column in df.columns for column in required_columns):
                    return HttpResponse("The Excel file is missing required columns.", status=400)

                # Process each row in the DataFrame

                for index, row in df.iterrows():
                    # Example: Create a new Client instance
                    phone_number = str(row['phone_number']).strip()
                    Client.objects.create(
                        name=row['name'],
                        email=row['email'],
                        national_id=row['national_id'],
                        phone_number=phone_number,
                        paid_money=row.get('paid_money', 0),
                        money_left=row.get('money_left', 0),
                        compnay=Company.objects.first()  # Replace with actual logic to assign the company
                    )
                
                return HttpResponse('File uploaded and clients imported successfully.')
            except Exception as e:
                # Handle any errors that occur during file processing
                return HttpResponse(f"Error processing file: {str(e)}", status=500)
        else:
            return HttpResponse('Form is not valid', status=400)
    else:
        form = UploadExcelFileForm()

    return render(request, 'upload_clients.html', {'form': form})















# all sessions in website 
class AllCompaniesAPi(ListAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        search_word = self.request.query_params.get('query_word', '').strip()
        search_word= search_word.strip()
        queryset = None
        if search_word:
            queryset = Company.objects.filter(Q(name__icontains=search_word) | Q(subdomain__icontains=search_word)

             )
        else:
            queryset = Company.objects.all()
        pagination = self.pagination_class()
        queryset = self.filter_queryset(queryset)
        paginated_queryset = pagination.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True,context={"request":request})
        response = pagination.get_paginated_response(serializer.data)
        

        # Customizing response data
        custom_data = {
            'results': response.data['results'],  # Include paginated results
            'count': response.data['count'],  # Include total count
            'next': response.data['next'],  # Include next page URL if available
            'previous': response.data['previous'],  # Include previous page URL if available
        }
        
        return Response(custom_data)




class AddCompanyView(CreateAPIView):
    serializer_class = AddCompanySerializer
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        required_fields = ['name','subdomain']
        for field in required_fields:
            if field not in request.data or not request.data[field]:
                message = f"مطلوب {field}"
                message = {field:[message]}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
        data = request.data
        company = Company.objects.filter(name=data['name']).first()
        if company:
            message = "company with same name already exists"
            message = {"message":message}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        company = Company.objects.filter(subdomain=data['subdomain']).first()
        if company:
            message = "company with same subdomain already exists"
            message = {"message":message}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        dataa = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = {"data":serializer.data,"message":"company created successfully"}
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
    




    

class AllClientsAPi(ListAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination  # Make sure to define a pagination class if needed

    def get_queryset(self):
        search_word = self.request.query_params.get('query_word', '').strip()
        company_id = self.request.query_params.get('company_id', '').strip()
        
        queryset = Client.objects.all()
        
        # If company_id is provided, filter by company
        if company_id:
            queryset = queryset.filter(companies__id=company_id)

        # If a search_word is provided, filter by search terms
        if search_word:
            queryset = queryset.filter(
                Q(national_id__icontains=search_word) |
                Q(name__icontains=search_word) |
                Q(email__icontains=search_word)
            )
        
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


def export_clients_excel(request, company_id):
    """Generate and serve Excel file for clients of a selected company."""
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return HttpResponse("Company not found", status=404)

    # Fetch clients associated with the selected company via many-to-many relationship
    clients = Client.objects.filter(companies__id=company.id)

    # Prepare data for export
    data = []
    for client in clients:
        created_at = client.created_at
        if is_aware(created_at):
            created_at = created_at.astimezone(timezone.utc).replace(tzinfo=None)

        data.append({
            'name': client.name,
            'national_id': client.national_id,
            'email': client.email,
            'phone_number': client.phone_number,
            'paid_money': client.paid_money,
            'money_left': client.money_left,
            'created_at': created_at  # Adding created_at for extra context
        })

    # Create a DataFrame using pandas
    df = pd.DataFrame(data)

    # Create an Excel file in memory
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{company.name}_clients.xlsx"'

    # Use pandas to write the DataFrame to an Excel file
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response










from rest_framework.views import APIView
class UploadClientsAPIView(APIView):
    def post(self, request, company_id, format=None):
        try:
            # Get the company by ID
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure a file is included in the request
        if 'file' not in request.FILES:
            return Response({"error": "File is required"}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']

        try:
            # Read the Excel file using pandas
            df = pd.read_excel(file)

            # Check for the required columns
            required_columns = ['name', 'national_id', 'email', 'phone_number', 'paid_money', 'money_left']
            if not all(column in df.columns for column in required_columns):
                return Response({"error": "Missing required columns in the file."}, status=status.HTTP_400_BAD_REQUEST)

            clients_to_attach = []
            for _, row in df.iterrows():
                # Check if the client already exists (by national_id or email)
                client = Client.objects.filter(national_id=row['national_id']).first() or \
                         Client.objects.filter(email=row['email']).first()

                if client:
                    # If client exists, attach them to the company (if not already attached)
                    if not client.companies.filter(id=company.id).exists():
                        client.companies.add(company)
                        clients_to_attach.append(client)
                else:
                    # Prepare new client data
                    client_data = {
                        'name': row['name'],
                        'national_id': row['national_id'],
                        'email': row['email'],
                        'phone_number': row['phone_number'],
                        'paid_money': row.get('paid_money', 0),
                        'money_left': row.get('money_left', 0)
                    }

                    # Validate and create the new client
                    serializer = ClientSerializer(data=client_data)
                    if serializer.is_valid():
                        client_instance = serializer.save()
                        client_instance.companies.add(company)  # Attach the new client to the company
                        clients_to_attach.append(client_instance)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Clients successfully processed", "clients": [client.id for client in clients_to_attach]},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Error processing file: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        














# auth apis
        

class LoginView(ObtainAuthToken):
    authentication_classes = []
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        required_fields = ["email","password"]
        filed_not_sent = check_required_fileds(required_fields,data)
        if filed_not_sent:
            return Response(default_error_response(message=filed_not_sent), status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)


        valid_user = User.objects.filter(
                                email=request.data["email"]).first()
        
        if not valid_user:
            message = _("email is not valid")
            return Response(default_error_response(message=message), status=status.HTTP_400_BAD_REQUEST)

        if not check_password(request.data['password'],valid_user.password ):
            message = _("password is not valid")
            return Response(default_error_response(message=message), status=status.HTTP_400_BAD_REQUEST)
   

        # serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data['user']
        # if not valid_user.mobile_verified:
        #     message = _("phone number need to be verified")
        #     return Response(default_error_response(message=message), status=status.HTTP_400_BAD_REQUEST)


        token, created = Token.objects.get_or_create(user=valid_user)
        request.user =valid_user
        # fcm_device_serializer = FCMDeviceSerializer(data=request.data["fcmdevice"], context={"request":request})
        # fcm_device_serializer.is_valid(raise_exception=True)
        # fcm_device_serializer.save()

        response_payload = {
            "name": valid_user.name,
            "email": valid_user.email,
            "token": token.key
        }
        message = _("logged in successfully")
        return Response(default_success_response(message=message,data=response_payload), status=status.HTTP_200_OK)




login_view = LoginView.as_view()



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    # def delete_fcm_token(self):
    #     registration_id = self.request.GET.get('registration_id', None)
    #     try:
    #         token_exists = FCMDevice.objects.filter(user=self.request.user, registration_id=registration_id).first()
    #         if token_exists:
    #             token_exists.delete()
    #     except TypeError:
    #         pass

    def delete_auth_token(self):
        self.request.user.auth_token.delete()

    def get(self, request):
        # self.delete_fcm_token()
        # self.delete_auth_token()
        # return Response(status=status.HTTP_200_OK)

        message = _("logged out successfully")
        return Response(default_success_response(message=message), status=status.HTTP_200_OK)



logout_view = LogoutView.as_view()




class ChangeUserPasswordView(UpdateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ChangePasswordSerializer
    model = User
    queryset = User.objects.all()
    
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        # Check old password
        if not self.object.check_password(serializer.data.get("old_password")):
            message = _("old password is not valid")
            return Response(default_error_response(message=message), status=status.HTTP_400_BAD_REQUEST)
   

        # valid_pass  = validate_password(serializer.data.get("new_password"))
        # if not valid_pass:
        #     message = _("password is not valid ,can not be less than 8 chars, and contain uppercase, 1 lowercase and 1 special char")
        #     return Response(default_error_response(message=message), status=status.HTTP_400_BAD_REQUEST)

            # return Response({"old_password": ["الرقم السري القديم غير صحيح."]}, status=status.HTTP_400_BAD_REQUEST)
        # set_password also hashes the password that the user will get
        self.object.set_password(serializer.data.get("new_password"))
        self.object.save()
        message = _("password changed successfully")
        return Response(default_success_response(message=message), status=status.HTTP_200_OK)

        # response = {
        #     'status': 'success',
        #     'code': status.HTTP_200_OK,
        #     'message': 'تم تحديث الرقم السري بنجاح.',
        #     'data': []
        # }

        # return Response(response)
    
change_password_view = ChangeUserPasswordView.as_view()



class CompanyAnalyticsAPIView(APIView):
    def get(self, request, company_id):
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        # Number of clients
        num_clients = company.clients.count()

        # Total money paid
        total_paid = Client.objects.filter(companies=company).aggregate(total_paid=Sum('paid_money'))['total_paid'] or 0

        # Total outstanding money (money left)
        total_outstanding = Client.objects.filter(companies=company).aggregate(total_outstanding=Sum('money_left'))['total_outstanding'] or 0

        # Average payment per client
        avg_payment = Client.objects.filter(companies=company).aggregate(avg_payment=Avg('paid_money'))['avg_payment'] or 0

        # Top 5 clients by payment
        top_clients = Client.objects.filter(companies=company).order_by('-paid_money')[:5]
        top_clients_data = [{
            'name': client.name,
            'paid_money': client.paid_money
        } for client in top_clients]

        # Total clients added this month
        current_month = now().month
        new_clients_this_month = Client.objects.filter(companies=company, created_at__month=current_month).count()

        # Total payments made this month
        payments_this_month = Client.objects.filter(companies=company, created_at__month=current_month).aggregate(total_paid=Sum('paid_money'))['total_paid'] or 0

        # Number of clients with outstanding payments
        clients_with_outstanding = Client.objects.filter(companies=company, money_left__gt=0).count()

        # Percentage of clients with complete payments
        if num_clients > 0:
            clients_paid_in_full = Client.objects.filter(companies=company, money_left=0).count()
            percentage_paid_in_full = (clients_paid_in_full / num_clients) * 100
        else:
            percentage_paid_in_full = 0

        # Highest paying client
        highest_paying_client = Client.objects.filter(companies=company).order_by('-paid_money').first()
        highest_paying_client_data = {
            'name': highest_paying_client.name,
            'paid_money': highest_paying_client.paid_money
        } if highest_paying_client else {}

        # Prepare response data
        data = {
            'num_clients': num_clients,
            'total_paid': total_paid,
            'total_outstanding': total_outstanding,
            'avg_payment': avg_payment,
            'top_clients': top_clients_data,
            'new_clients_this_month': new_clients_this_month,
            'payments_this_month': payments_this_month,
            'clients_with_outstanding': clients_with_outstanding,
            'percentage_paid_in_full': percentage_paid_in_full,
            'highest_paying_client': highest_paying_client_data
        }

        serializer = CompanyAnalyticsSerializer(data=data)
        serializer.is_valid()  # No need to save, as it's not a model
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class ClientByNationalIdAPIView(RetrieveAPIView):
    serializer_class = ClientSerializer
    permission_classes = []

    def get_object(self):
        # Get the national_id from the request's URL parameters
        national_id = self.kwargs.get('national_id')

        # Try to get the client by the provided national_id or return 404 if not found
        client = get_object_or_404(Client, national_id=national_id)
        return client

    def get(self, request, *args, **kwargs):
        client = self.get_object()
        serializer = self.get_serializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK)