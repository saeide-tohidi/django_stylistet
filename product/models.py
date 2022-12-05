from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.text import slugify
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _

from attribute.models import unique_slugify
from seo.models import SeoModel
from django_prices.models import MoneyField
from babel.numbers import list_currencies


def create_currency():
    currency_choices = [(currency, currency) for currency in list_currencies()]
    return sorted(currency_choices, key=lambda x: x[0])


class ProductCategory(MPTTModel):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, blank=True)
    description = models.TextField(blank=True, null=True)
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
        verbose_name=_("Parent"),
    )
    background_image = models.ImageField(
        upload_to="category-backgrounds", blank=True, null=True
    )
    background_image_alt = models.CharField(max_length=128, blank=True)

    seo_title = models.CharField(
        max_length=70, blank=True, null=True, validators=[MaxLengthValidator(70)]
    )
    seo_description = models.CharField(
        max_length=300, blank=True, null=True, validators=[MaxLengthValidator(300)]
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            lower_name = self.name.lower()
            self.slug = unique_slugify(self, lower_name)
        super(ProductCategory, self).save(*args, **kwargs)


class ProductType(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, blank=True)

    class Meta:
        ordering = ("slug",)
        app_label = "product"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            lower_name = self.name.lower()
            self.slug = unique_slugify(self, lower_name)
        super(ProductType, self).save(*args, **kwargs)

    def __repr__(self) -> str:
        class_ = type(self)
        return "<%s.%s(pk=%r, name=%r)>" % (
            class_.__module__,
            class_.__name__,
            self.pk,
            self.name,
        )


class Product(SeoModel):
    product_type = models.ForeignKey(
        "ProductType", related_name="products", on_delete=models.CASCADE
    )
    product_category = models.ForeignKey(
        "ProductCategory",
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=250)
    main_image = models.ImageField(upload_to="products", blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, blank=True)
    description = models.TextField(blank=True, null=True)
    currency = models.CharField(max_length=3, default="AED", choices=create_currency())
    price_amount = models.DecimalField(
        _("Price"), max_digits=9, decimal_places=2, default="0"
    )
    price = MoneyField(amount_field="price_amount", currency_field="currency")
    shopping_url = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        app_label = "product"
        ordering = ("slug",)

    def __str__(self):
        return self.name

    @property
    def get_attr_values(self):
        attributes = self.attributes.all()
        all_attr_val = []
        all_attr_val_str = ""

        for attr in attributes:
            values = []
            values_str = ""
            for at in attr.productvalueassignment.all():
                values.append([at.value.name])
                values_str = f"{values_str} {at.value.name},"
            t = f"{attr.attribute.name}: {values_str} "
            all_attr_val.append(t)
            all_attr_val_str = f"{all_attr_val_str}{t} _ "

        return all_attr_val

    @property
    def get_values(self):
        attributes = self.attributes.v

        return attributes


class ProductMedia(models.Model):
    product = models.ForeignKey(
        "Product",
        related_name="media",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to="products", blank=True, null=True)
    alt = models.CharField(max_length=128, blank=True)
    external_url = models.CharField(max_length=256, blank=True, null=True)
    to_remove = models.BooleanField(default=False)

    class Meta:
        ordering = ("pk",)
        app_label = "product"
