from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from commcare_connect.users.forms import OrganizationCreationForm, UserAdminChangeForm, UserAdminCreationForm
from commcare_connect.users.models import Organization, UserOrganizationMembership

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "name", "is_superuser"]
    search_fields = ["name"]
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


class UserOrganizationMembershipInline(admin.TabularInline):
    list_display = ["organization", "user", "role"]
    model = UserOrganizationMembership


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    form = OrganizationCreationForm
    list_display = ["name", "created_by"]
    search_fields = ["name"]
    ordering = ["name"]
    inlines = [UserOrganizationMembershipInline]

