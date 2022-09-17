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


class AttributeAdmin(admin.ModelAdmin):
    model = Attribute

    inlines = [
        AttributeValueInline,
    ]


admin.site.register(Attribute, AttributeAdmin)

admin.site.register(AssignedProductAttribute)
admin.site.register(AttributeProduct)
admin.site.register(AssignedProductAttributeValue)
