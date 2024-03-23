from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, Group, Permission
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager
import pytz
from datetime import datetime


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("Username"), max_length=50, unique=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    objects = UserManager()

    def __str__(self):
        return str(self.email)

    class Meta:
        db_table = "users"

    def save(self, *args, **kwargs):

        super(User, self).save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        related_name="profile",
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(_("First name"), max_length=40, null=True, blank=True)
    last_name = models.CharField(_("Last name"), max_length=40, null=True, blank=True)
    picture = models.ImageField(_("Picture"), blank=True, null=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name}  {self.last_name}"
        elif self.user.username:
            return self.user.username
        return self.user.email


class UserBits(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        related_name="bits",
        on_delete=models.CASCADE,
    )
    last_login = models.DateTimeField(_("Last login in app"), null=True, blank=True)

    def __str__(self):
        return str(self.user.email)

    def record_last_login(self):
        self.last_login_chat_room = datetime.now()
        self.save()


class UserConfig(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        related_name="config",
        on_delete=models.CASCADE,
    )

    TIMEZONES = [(t, t) for t in pytz.all_timezones]
    user_timezone = models.CharField(
        _("Timezone"), choices=TIMEZONES, max_length=100, default="Canada/Central"
    )
    timezone_setted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.email)

    def save(self, *args, **kwargs):

        super(UserConfig, self).save(*args, **kwargs)


class UserPreference(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        related_name="preference",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.user.email)


class UserPreferenceInstanceCollectionAttribute(models.Model):
    user_preference = models.ForeignKey(
        "account.UserPreference",
        verbose_name=_("User"),
        related_name="instance_collection_attribute",
        on_delete=models.CASCADE,
    )

    ATTRIBUTE_COLLECTION = "collection"
    ATTRIBUTE_PRODUCT = "product"
    ATTRIBUTE_TYPES = (
        (ATTRIBUTE_COLLECTION, "Collection"),
        (ATTRIBUTE_PRODUCT, "Product"),
    )
    attribute = models.ForeignKey(
        "collection.CollectionAttribute",
        related_name="preference_collection",
        on_delete=models.CASCADE,
    )

    values = models.ManyToManyField(
        "collection.CollectionAttributeValue",
        blank=True,
        related_name="collectionattributeinstance",
        through="UserPreferenceInstanceCollectionAttributeValue",
    )

    class Meta:
        unique_together = (("user_preference", "attribute"),)

    def __str__(self):
        return str(self.user_preference)


class UserPreferenceInstanceCollectionAttributeValue(models.Model):
    value = models.ForeignKey(
        "collection.CollectionAttributeValue",
        on_delete=models.CASCADE,
        related_name="collectionvalueassignment_user",
    )
    instance = models.ForeignKey(
        "account.UserPreferenceInstanceCollectionAttribute",
        on_delete=models.CASCADE,
        related_name="collectionattrvalueassignment_user",
    )

    class Meta:
        unique_together = (("value", "instance"),)
        ordering = ("pk",)

    def __str__(self):
        return str(self.value)
