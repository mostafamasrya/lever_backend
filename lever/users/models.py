
from typing import ClassVar
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField , FloatField,FileField
from django.db.models import EmailField,BooleanField, DateTimeField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator, MinLengthValidator, MaxLengthValidator, RegexValidator
from .managers import UserManager
import random
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.utils.translation import gettext as _

class User(AbstractUser):
    """
    Default custom user model for hareefa.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), max_length=255)

    email = EmailField(_("email address"), unique=True, validators=[
        RegexValidator(regex=r'^(?![.-])[a-zA-Z0-9._%+-]+(?<![.-])@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                       message=_("Enter a valid email address."))
        ])
    phone_number = PhoneNumberField(_("Phone Number of user"),unique=True,blank=True,null=True)
    longitute = FloatField(_("longitute value"),blank=True,null=True)
    latitute = FloatField(_("latitute value"),blank=True,null=True)
    mobile_verified = BooleanField(_("mobile_verified ?"),default=False)

    date_deleted = DateTimeField(_("date when user has been deleted"),blank=True,null=True)
    profile_image = FileField(_("profile image of user"),upload_to="Users_images/", null=True, blank=True,
                                    validators=[
                                        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpg', 'jpeg', 'webp'])],
                                    help_text=_("The image representing profile of user"))

    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})




class Company(models.Model):
    name = models.CharField(_('company name'), max_length=256,unique=True)
    subdomain = models.CharField(_('Company Subdomain'), max_length=256,unique=True)
    created_at = models.DateTimeField(_('craeted at'),default=timezone.now)

    def __str__(self):
        return "Company  : " + self.name


class Client(models.Model):
    name = models.CharField(_('Client name'), max_length=256)
    national_id = models.CharField(_('Client ID'), max_length=256,unique=True)
    email = EmailField(_("email address"), unique=True, validators=[
        RegexValidator(regex=r'^(?![.-])[a-zA-Z0-9._%+-]+(?<![.-])@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                       message=_("Enter a valid email address."))
        ])
    phone_number = PhoneNumberField(_("Phone Number of user"),unique=True,blank=True,null=True)
    paid_money = models.FloatField(_('Money which user already paid '),default=0,null=True,blank=True)
    money_left = models.FloatField(_('left Money which user must  pay '),default=0,null=True,blank=True)

    created_at = models.DateTimeField(_('craeted at'),default=timezone.now)
    companies = models.ManyToManyField(Company, through='ClientCompany', related_name='clients',null=True,blank=True)

    def __str__(self):
        return "Client  : " + self.name
    



class ClientCompany(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_companies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_clients')
    class Meta:
        unique_together = ('client', 'company')
        verbose_name = _('Client-Company Relationship')
        verbose_name_plural = _('Client-Company Relationships')

    def __str__(self):
        return f"{self.client.name} associated with {self.company.name}"


