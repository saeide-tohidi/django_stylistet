from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, Group, Permission
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("Username"), max_length=50, unique=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "email",
    ]

    objects = UserManager()

    def __str__(self):
        return str(self.email)

    class Meta:
        db_table = "users"

    def save(self, *args, **kwargs):

        super(User, self).save(*args, **kwargs)
