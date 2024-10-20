# from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _
from django.urls import path
from django import forms
from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import User,Company,Client,ClientCompany
from rest_framework.authtoken.models import Token
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.timezone import is_aware, timezone
import pandas as pd
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
# if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
#     # Force the `admin` sign in process to go through the `django-allauth` workflow:
#     # https://docs.allauth.org/en/latest/common/admin.html#admin
#     admin.autodiscover()
#     admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]


class UploadExcelFileForm(forms.Form):
    file = forms.FileField()

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    # Fieldsets for organizing the fields in sections
    fieldsets = (
        (_("Personal Information"), {
            "fields": ("email", "name", "phone_number",  "longitute",
                       "latitute", "mobile_verified", "profile_image", 'date_deleted')}),
    )

    readonly_fields = ("token", )
    
    # Fields to display in the admin list view
    list_display = ["id", "email", "name", "mobile_verified"]
    
    # Ordering of the displayed items
    ordering = ["id"]

    # Fields for adding new users
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email","phone_number", "password1", "password2", "username")}),
    )
    
    def token(self, obj):
        """
        Returns the token associated with the user.
        """
        try:
            token = Token.objects.get(user=obj)
            return token.key
        except Token.DoesNotExist:
            return _('No Token')

    token.short_description = 'Auth Token'  # Set display name in the admin panel




@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    
    # Registering actions
    actions = ['export_clients_action', 'upload_clients_action']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-clients/<int:company_id>/', self.admin_site.admin_view(self.export_clients_excel), name='export_clients_excel'),
        ]
        return custom_urls + urls

    def export_clients_action(self, request, queryset):
        """Redirect to download link for the selected company."""
        if queryset.count() != 1:
            self.message_user(request, "Please select exactly one company to export clients.", level=messages.ERROR)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # Get the company ID and redirect to the export URL
        company = queryset.first()
        download_url = reverse('admin:export_clients_excel', args=[company.id])
        return HttpResponseRedirect(download_url)

    export_clients_action.short_description = "Export Clients to Excel"

    def export_clients_excel(self, request, company_id):
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
                'money_left': client.money_left
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

    export_clients_action.short_description = "Export Clients to Excel"

    def upload_clients_action(self, request, queryset):
        """Upload clients from Excel file via admin action."""
        print("upload 1111111111")
        if 'apply' in request.POST:
            print("POST request received")
            form = UploadExcelFileForm(request.POST, request.FILES)
            print(f"Form files: {request.FILES}")  # Debugging line
            if form.is_valid():
                print("Form is valid")
                file = request.FILES['file']
                print(f"Uploaded file: {file}")  # Debugging line
                try:
                    # Read the Excel file using pandas
                    df = pd.read_excel(file)

                    # Check required columns exist in the file
                    required_columns = ['name', 'national_id', 'email', 'phone_number', 'paid_money', 'money_left']
                    if not all(column in df.columns for column in required_columns):
                        messages.error(request, "Missing required columns in the file.")
                        return redirect('admin:users_company_changelist')

                    for company in queryset:
                        # Loop over the rows in the Excel and create clients
                        for _, row in df.iterrows():
                            Client.objects.create(
                                name=row['name'],
                                national_id=row['national_id'],
                                email=row['email'],
                                phone_number=row['phone_number'],
                                paid_money=row.get('paid_money', 0),
                                money_left=row.get('money_left', 0),
                                compnay=company
                            )

                    messages.success(request, "Clients successfully imported.")
                    return redirect('admin:users_company_changelist')
                except Exception as e:
                    print("upload Exception :: ", e)
                    messages.error(request, f"Error processing file: {e}")
                    return redirect('admin:users_company_changelist')
            else:
                print(f"Form errors: {form.errors}")  # This will print form errors if the form is invalid
        else:
            print("upload else 00000000000000000")
            form = UploadExcelFileForm()

        # Display the file upload form for the selected companies
        return render(request, 'upload_clients.html', {'companies': queryset, 'form': form})

    upload_clients_action.short_description = "Upload Clients from Excel"

    list_display = ('id','name', 'subdomain')



    # Fields to search by
    search_fields = ('name', 'subdomain')

    # Organize fields in sections
    fieldsets = (
        (None, {
            'fields': ('name', 'subdomain','created_at')}),
    )





@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('id','name','national_id'
                   ,'paid_money', 'money_left')

    # Filters for the list view
    list_filter = ( 'paid_money','money_left')

    # Fields to search by
    search_fields = ('name', 'national_id')

    # Organize fields in sections
    fieldsets = (
        (None, {
            'fields': ('name','national_id', 'email',
                    'phone_number','paid_money', 'money_left','created_at')}),
    )





@admin.register(ClientCompany)
class ClientCompanyAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('id','company','client')

    # Filters for the list view
    list_filter = ( 'company',)

    # Fields to search by
    search_fields = ('client', 'company')

    # Organize fields in sections
    fieldsets = (
        (None, {
            'fields': ('company','client')}),
    )