from django.db import models
from product.models import ProductType, Product


class AttributeInputType:
    """The type that we expect to render the attribute's values as."""

    DROPDOWN = "dropdown"
    MULTISELECT = "multiselect"
    FILE = "file"
    NUMERIC = "numeric"
    PLAIN_TEXT = "plain-text"
    BOOLEAN = "boolean"

    CHOICES = [
        (DROPDOWN, "Dropdown"),
        (MULTISELECT, "Multi Select"),
        (FILE, "File"),
        (NUMERIC, "Numeric"),
        (PLAIN_TEXT, "Plain Text"),
        (BOOLEAN, "Boolean"),
    ]

    # list of the input types that can be used in variant selection
    ALLOWED_IN_VARIANT_SELECTION = [DROPDOWN, BOOLEAN, NUMERIC]

    TYPES_WITH_CHOICES = [
        DROPDOWN,
        MULTISELECT,
    ]

    # list of the input types that are unique per instances
    TYPES_WITH_UNIQUE_VALUES = [
        FILE,
        PLAIN_TEXT,
        NUMERIC,
    ]

    # list of the translatable attributes, excluding attributes with choices.
    TRANSLATABLE_ATTRIBUTES = [
        PLAIN_TEXT,
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
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True)
    name = models.CharField(max_length=255)

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
    visible_in_storefront = models.BooleanField(default=True, blank=True)

    filterable_in_storefront = models.BooleanField(default=False, blank=True)
    filterable_in_dashboard = models.BooleanField(default=False, blank=True)

    storefront_search_position = models.IntegerField(default=0, blank=True)
    available_in_grid = models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ("slug",)

    def __str__(self) -> str:
        return self.name

    def has_values(self) -> bool:
        return self.values.exists()


class AttributeValue(models.Model):
    name = models.CharField(max_length=250)
    picture = models.ImageField(blank=True, null=True)

    # keeps hex code color value in #RRGGBBAA format
    value = models.CharField(max_length=100, blank=True, default="")
    slug = models.SlugField(max_length=255, allow_unicode=True)
    file_url = models.URLField(null=True, blank=True)
    content_type = models.CharField(max_length=50, null=True, blank=True)
    attribute = models.ForeignKey(
        "Attribute", related_name="values", on_delete=models.CASCADE
    )
    plain_text = models.TextField(
        blank=True,
        null=True,
    )
    boolean = models.BooleanField(blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ("pk",)
        unique_together = ("slug", "attribute")

    def __str__(self) -> str:
        return self.name

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
