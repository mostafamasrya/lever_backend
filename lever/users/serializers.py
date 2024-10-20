from django.utils import timezone
# from django.utils.datetime_safe import datetime
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from lever.users.models import * 
from datetime import datetime
import random
from django.contrib.auth import get_user_model, authenticate
import pytz

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id',
            'name',
            'national_id',
            'email',
            'phone_number',
            'paid_money',
            'money_left',
            'created_at',
            'companies'  # Assuming you want to include the associated companies
        ]
        read_only_fields = ['id', 'created_at']  # Make `id` and `created_at` read-only

    # Serialize the companies field to show company details
    companies = serializers.StringRelatedField(many=True)





class AddCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'name', 'subdomain'
        ]


    def create(self, validated_data):
        user_related_data = {
            'name': validated_data.get('name'),
            'subdomain': validated_data.get('subdomain'),
            
        }

        company = self.Meta.model.objects.create(**user_related_data)
       
        return company
    
  


class AuthTokenSerializer(serializers.Serializer):
    # email = serializers.EmailField(
    #     label=_("Email"),
    #     trim_whitespace=True
    # )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )
    type = serializers.CharField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = _('البريد الإلكتروني او كلمة المرور غير صحيحة')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        self.context.get('request').user = user

        # Create FCM Device related to this user through
        # fcm_device_data = attrs.get('fcmdevice')
        # fcm_device_serializer = FCMDeviceSerializer(data=fcm_device_data, context=self.context)
        # fcm_device_serializer.is_valid(raise_exception=True)
        # fcm_device_serializer.save()

        attrs['user'] = user
        return attrs
    


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)






class CompanyAnalyticsSerializer(serializers.Serializer):
    num_clients = serializers.IntegerField()
    total_paid = serializers.FloatField()
    total_outstanding = serializers.FloatField()
    avg_payment = serializers.FloatField()
    top_clients = serializers.ListField(child=serializers.DictField())
    new_clients_this_month = serializers.IntegerField()
    payments_this_month = serializers.FloatField()
    clients_with_outstanding = serializers.IntegerField()
    percentage_paid_in_full = serializers.FloatField()
    highest_paying_client = serializers.DictField()