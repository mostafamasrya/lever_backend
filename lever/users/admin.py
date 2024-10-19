# from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import User
from rest_framework.authtoken.models import Token

# if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
#     # Force the `admin` sign in process to go through the `django-allauth` workflow:
#     # https://docs.allauth.org/en/latest/common/admin.html#admin
#     admin.autodiscover()
#     admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]
@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    
    # Fieldsets for organizing the fields in sections
    fieldsets = (
        (_("Personal Information"), {
            "fields": ("email", "name", "phone_number",  "longitute",
                       "latitute", "mobile_verified", "profile_image", 'date_deleted')}),
        # (_("Financial Information"), {
        #     "fields": ("bank_account_number", "payout_method", )
        #     }),
        # (_("Admin Dashboard Permissions"), {
        #     "fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
        # (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        # (_('Token'), {'fields': ('token',)}),
    )

    readonly_fields = ("token", )
    
    # Fields to display in the admin list view
    list_display = ["id", "email", "name", "mobile_verified"]
    
    # Filters for the list view
    # list_filter = ["type", "is_superuser", "is_active", "joined_at", "grade", "assistant_active"]

    # # Fields to search by
    # search_fields = ["email", "phone_number", ]
    
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

