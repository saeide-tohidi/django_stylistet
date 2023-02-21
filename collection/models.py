from django.db import models
from django.utils.text import slugify
import pathlib

from attribute.models import AttributeProduct, AttributeValue
from product.models import ProductType, Product
from django.utils.crypto import get_random_string
from seo.models import SeoModel


def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + "-" + get_random_string(length=4)
    return unique_slug


class AttributeInputType:
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


class Collection(SeoModel):
    name = models.CharField(max_length=250)
    main_image = models.ImageField(upload_to="collections", blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        app_label = "collection"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        lower_name = self.name.lower()

        if not self.slug:
            self.slug = unique_slugify(self, lower_name)

        super(Collection, self).save(*args, **kwargs)

    @property
    def get_items(self):
        return self.items.all()


class CollectionAttribute(models.Model):
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
    value_required = models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ("slug",)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            lower_name = self.name.lower()
            self.slug = unique_slugify(self, lower_name)
        super(CollectionAttribute, self).save(*args, **kwargs)

    def has_values(self) -> bool:
        return self.values.exists()


class BaseAssignedAttribute(models.Model):
    assignment = None

    class Meta:
        abstract = True

    #
    # @property
    # def attribute(self):
    #     return self.assignment.id
    #
    # @property
    # def attribute_pk(self):
    #     return self.assignment.attribute_id


class CollectionAttributeValue(models.Model):
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
        "CollectionAttribute", related_name="values", on_delete=models.CASCADE
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

        super(CollectionAttributeValue, self).save(*args, **kwargs)

    @property
    def input_type(self):
        return self.attribute.input_type

    def get_ordering_queryset(self):
        return self.attribute.values.all()


class AssignedCollectionAttribute(BaseAssignedAttribute):
    collection = models.ForeignKey(
        Collection, related_name="attributes", on_delete=models.CASCADE
    )
    attribute = models.ForeignKey(
        CollectionAttribute,
        related_name="attributecollection",
        on_delete=models.CASCADE,
    )

    values = models.ManyToManyField(
        "CollectionAttributeValue",
        blank=True,
        related_name="collectionassignments",
        through="AssignedCollectionAttributeValue",
    )

    class Meta:
        unique_together = (("collection", "attribute"),)


class AssignedCollectionAttributeValue(models.Model):
    value = models.ForeignKey(
        CollectionAttributeValue,
        on_delete=models.CASCADE,
        related_name="collectionvalueassignment",
    )
    assignment = models.ForeignKey(
        AssignedCollectionAttribute,
        on_delete=models.CASCADE,
        related_name="collectionattrvalueassignment",
    )

    class Meta:
        unique_together = (("value", "assignment"),)
        ordering = ("pk",)

    def get_ordering_queryset(self):
        return self.assignment.collectionattrvalueassignment.all()

    def __str__(self):
        return str(self.value)


class Item(models.Model):
    name = models.CharField(max_length=250, null=True)
    collection = models.ForeignKey(
        "Collection", related_name="items", on_delete=models.CASCADE
    )
    product_type = models.ForeignKey(
        ProductType, related_name="product_type_items", on_delete=models.CASCADE
    )

    @property
    def get_attr_values(self):
        attributes = self.attributes.all()
        all_attr_val = []
        all_attr_val_str = ""

        for attr in attributes:
            values = []
            values_str = ""
            for at in attr.itemvalueassignment.all():
                values.append([at.value.name])
                values_str = f"{values_str} {at.value.name},"
            t = f"{attr.assignment.attribute.name}: {values_str} "
            all_attr_val.append(t)
            all_attr_val_str = f"{all_attr_val_str}{t} _ "

        return all_attr_val


class AssignedItemAttribute(BaseAssignedAttribute):
    """Associate a product type attribute and selected values to a given product."""

    item = models.ForeignKey(Item, related_name="attributes", on_delete=models.CASCADE)
    assignment = models.ForeignKey(
        AttributeProduct, on_delete=models.CASCADE, related_name="itemassignments"
    )
    values = models.ManyToManyField(
        AttributeValue,
        blank=True,
        related_name="itemproductassignments",
        through="AssignedItemAttributeValue",
    )

    class Meta:
        unique_together = (("item", "assignment"),)


class AssignedItemAttributeValue(models.Model):
    value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="itemvalueassignment",
    )
    assignment = models.ForeignKey(
        AssignedItemAttribute,
        on_delete=models.CASCADE,
        related_name="itemvalueassignment",
    )

    class Meta:
        unique_together = (("value", "assignment"),)
        ordering = ("pk",)

    def get_ordering_queryset(self):
        return self.assignment.itemvalueassignment.all()

    def __str__(self):
        return str(self.value)
