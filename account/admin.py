from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from account.models import User


class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "email",
        "username",
        "is_staff",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "username",
                    "password",
                    "date_joined",
                    "last_login",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("is_staff", "user_permissions", "groups"), "classes": ("",)},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_staff",
                ),
            },
        ),
    )
    list_filter = (
        "is_staff",
        "is_superuser",
    )
    search_fields = ("email",)
    readonly_fields = ("date_joined", "last_login")


admin.site.register(User, CustomUserAdmin)
