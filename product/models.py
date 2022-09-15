from django.db import models
from mptt.managers import TreeManager
from mptt.models import MPTTModel
from django.utils.translation import gettext_lazy as _
from seo.models import SeoModel
from django_prices.models import MoneyField
from babel.numbers import list_currencies


def create_currency():
    currency_choices = [(currency, currency) for currency in list_currencies()]
    return sorted(currency_choices, key=lambda x: x[0])


class ProductCategory(MPTTModel, SeoModel):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    background_image = models.ImageField(
        upload_to="category-backgrounds", blank=True, null=True
    )
    background_image_alt = models.CharField(max_length=128, blank=True)

    objects = models.Manager()
    tree = TreeManager()

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)

    class Meta:
        ordering = ("slug",)
        app_label = "product"

    def __str__(self):
        return self.name

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
    currency = models.CharField(max_length=3, default="USD", choices=create_currency())
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
        for attr in attributes:
            vals = []
            for at in attr.productvalueassignment.all():
                vals.append([at.value.name, at.value.id])
            t = f"{attr.attribute.name}: {vals} "
            all_attr_val.append(t)

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
