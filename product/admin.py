from django.contrib import admin

from attribute.models import AssignedProductAttribute, AttributeProduct
from product.models import ProductCategory, ProductMedia, ProductType, Product


class AttributeProductInline(admin.StackedInline):
    model = AttributeProduct


class ProductMediaInline(admin.StackedInline):
    model = ProductMedia


class ProductAdmin(admin.ModelAdmin):
    model = Product

    inlines = [
        ProductMediaInline,
    ]


class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType

    inlines = [
        AttributeProductInline,
    ]


admin.site.register(ProductMedia)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(ProductCategory)
