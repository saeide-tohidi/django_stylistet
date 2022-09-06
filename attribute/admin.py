from django.contrib import admin
from attribute.models import (
    Attribute,
    AttributeValue,
    AttributeProduct,
    AssignedProductAttribute,
    AssignedProductAttributeValue,
)

admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(AssignedProductAttribute)
admin.site.register(AttributeProduct)
admin.site.register(AssignedProductAttributeValue)
