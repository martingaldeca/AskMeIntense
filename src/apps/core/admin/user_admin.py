from core.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class AskMeIntenseUserAdmin(UserAdmin):
    fieldsets = (
        (_("Base info"), {"fields": ("email", "password", "uuid", "auth_provider")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "birthdate",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined", "created", "modified")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff"),
            },
        ),
    )

    list_display = [
        "id",
        "uuid",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_verified",
        "auth_provider",
    ]
    list_filter = [
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
    ]
    search_fields = ["first_name", "last_name", "email", "id", "uuid"]
    readonly_fields = ["date_joined", "last_login", "uuid", "id", "created", "modified"]
    ordering = ["created"]
