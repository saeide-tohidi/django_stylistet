from django.contrib import admin
from attribute.models import (
    Attribute,
    AttributeValue,
    AttributeProduct,
    AssignedProductAttribute,
    AssignedProductAttributeValue,
)


class AttributeValueInline(admin.StackedInline):
    model = AttributeValue
    readonly_fields = ["slug", "value"]


class AttributeAdmin(admin.ModelAdmin):
    model = Attribute
    fields = [
        "name",
        "input_type",
        "image_value",
        "value_required",
        "slug",
        "get_product_type_name",
    ]
    list_display = [
        "name",
        "input_type",
        "image_value",
        "value_required",
        "get_values_list",
        "get_values_count",
        "get_product_type_name",
    ]
    readonly_fields = [
        "get_values_count",
        "get_values_list",
        "slug",
        "get_product_type_name",
    ]
    inlines = [
        AttributeValueInline,
    ]

    def get_values_count(self, obj):
        return obj.values.count()

    get_values_count.allow_tags = True
    get_values_count.short_description = "All values count"

    def get_values_list(self, obj):
        val_list = []
        for val in obj.values.all():
            val_list.append(val.name)
        return val_list

    get_values_list.allow_tags = True
    get_values_list.short_description = "All values name"

    def get_product_type_name(self, obj):
        val_list = []
        for val in obj.product_types.all():
            val_list.append(val.name)
        return val_list

    get_product_type_name.allow_tags = True
    get_product_type_name.short_description = "get_product_type_name"


admin.site.register(Attribute, AttributeAdmin)

admin.site.register(AssignedProductAttribute)
admin.site.register(AttributeProduct)
admin.site.register(AssignedProductAttributeValue)
