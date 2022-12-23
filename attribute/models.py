from django.db import models
from django.utils.text import slugify
import pathlib
from product.models import ProductType, Product
from django.utils.crypto import get_random_string


def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + "-" + get_random_string(length=4)
    return unique_slug


class AttributeInputType:
    """The type that we expect to render the attribute's values as."""

    DROPDOWN = "oneselect"
    MULTISELECT = "multiselect"
    BOOLEAN = "boolean"

    CHOICES = [
        (DROPDOWN, "One select"),
        (MULTISELECT, "Multi Select"),
        (BOOLEAN, "Boolean"),
    ]

    # list of the input types that can be used in variant selection
    ALLOWED_IN_VARIANT_SELECTION = [DROPDOWN, BOOLEAN]

    TYPES_WITH_CHOICES = [
        DROPDOWN,
        MULTISELECT,
    ]


class BaseAssignedAttribute(models.Model):
    assignment = None

    class Meta:
        abstract = True

    @property
    def attribute(self):
        return self.assignment.attribute

    @property
    def attribute_pk(self):
        return self.assignment.attribute_id


class Attribute(models.Model):
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True, blank=True)
    name = models.CharField(max_length=255)
    image_value = models.BooleanField(
        default=False,
        help_text="If values for this attribute have image, select this item.",
    )

    input_type = models.CharField(
        max_length=50,
        choices=AttributeInputType.CHOICES,
        default=AttributeInputType.DROPDOWN,
    )

    product_types = models.ManyToManyField(
        ProductType,
        blank=True,
        related_name="product_attributes",
        through="AttributeProduct",
        through_fields=("attribute", "product_type"),
    )

    value_required = models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ("slug",)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            lower_name = self.name.lower()
            self.slug = unique_slugify(self, lower_name)
        super(Attribute, self).save(*args, **kwargs)

    def has_values(self) -> bool:
        return self.values.exists()


class AttributeValue(models.Model):
    name = models.CharField(max_length=250, blank=True)
    picture = models.ImageField(blank=True, null=True)
    value = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="keeps hex code color value in #RRGGBBAA format",
    )
    slug = models.SlugField(max_length=255, allow_unicode=True, blank=True)
    attribute = models.ForeignKey(
        "Attribute", related_name="values", on_delete=models.CASCADE
    )
    boolean = models.BooleanField(blank=True, null=True)

    class Meta:
        ordering = ("pk",)
        unique_together = ("slug", "attribute")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            pic_name = str(self.picture)
            pic_suffix = pathlib.Path(pic_name).suffix
            name = (
                pic_name.replace(pic_suffix, "")
                .replace(".", " ")
                .replace("-", " ")
                .replace("_", " ")
            )
            self.name = name
        lower_name = self.name.lower()

        if not self.slug:
            self.slug = unique_slugify(self, lower_name)

        if not self.value:
            self.value = self.slug

        super(AttributeValue, self).save(*args, **kwargs)

    @property
    def input_type(self):
        return self.attribute.input_type

    def get_ordering_queryset(self):
        return self.attribute.values.all()


class AssignedProductAttribute(BaseAssignedAttribute):
    """Associate a product type attribute and selected values to a given product."""

    product = models.ForeignKey(
        Product, related_name="attributes", on_delete=models.CASCADE
    )
    assignment = models.ForeignKey(
        "AttributeProduct", on_delete=models.CASCADE, related_name="productassignments"
    )
    values = models.ManyToManyField(
        "AttributeValue",
        blank=True,
        related_name="productassignments",
        through="AssignedProductAttributeValue",
    )

    class Meta:
        unique_together = (("product", "assignment"),)


class AttributeProduct(models.Model):
    attribute = models.ForeignKey(
        Attribute, related_name="attributeproduct", on_delete=models.CASCADE
    )
    product_type = models.ForeignKey(
        ProductType, related_name="attributeproduct", on_delete=models.CASCADE
    )
    assigned_products = models.ManyToManyField(
        Product,
        blank=True,
        through=AssignedProductAttribute,
        through_fields=("assignment", "product"),
        related_name="attributesrelated",
    )

    def __str__(self):
        return "___" + self.attribute.name

    class Meta:
        unique_together = (("attribute", "product_type"),)
        ordering = ("pk",)

    def get_ordering_queryset(self):
        return self.product_type.attributeproduct.all()


class AssignedProductAttributeValue(models.Model):
    value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="productvalueassignment",
    )
    assignment = models.ForeignKey(
        AssignedProductAttribute,
        on_delete=models.CASCADE,
        related_name="productvalueassignment",
    )

    class Meta:
        unique_together = (("value", "assignment"),)
        ordering = ("pk",)

    def get_ordering_queryset(self):
        return self.assignment.productvalueassignment.all()

    def __str__(self):
        return str(self.value)
