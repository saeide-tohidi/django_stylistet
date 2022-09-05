from rest_framework import serializers
from account.models import UserProfile, User
from django.contrib.auth.password_validation import validate_password


class UserRegisterSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
    )
    email = serializers.CharField(
        required=True,
    )
    username = serializers.CharField(
        required=True,
    )

    class Meta:
        model = User
        fields = ["email", "username", "password", "re_password"]
        extra_kwargs = {"password": {"write_only": True}}


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
