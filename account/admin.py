from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User, UserProfile
from rest_framework.authtoken.models import Token


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class TokenInline(admin.StackedInline):
    model = Token


class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ("email", "username", "is_staff", "get_token")
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
    search_fields = ("email", "username", "auth_token__key")
    readonly_fields = ("date_joined", "last_login")

    inlines = [
        TokenInline,
        UserProfileInline,
    ]

    def get_token(self, obj):
        return obj.auth_token.key

    get_token.short_description = "Token"


admin.site.register(User, CustomUserAdmin)
