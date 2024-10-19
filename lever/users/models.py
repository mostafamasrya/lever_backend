
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