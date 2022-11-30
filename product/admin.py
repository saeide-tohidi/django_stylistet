from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
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
    list_display = ["name", "get_attribute_product"]
    readonly_fields = ["slug", "get_attribute_product"]
    inlines = [
        AttributeProductInline,
    ]

    def get_attribute_product(self, obj):
        attr_list = []
        for val in obj.attributeproduct.all():
            attr_list.append(val.attribute.name)
        return attr_list

    get_attribute_product.allow_tags = True
    get_attribute_product.short_description = "All attributes"


class ProductCategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    expand_tree_by_default = True
    MPTT_ADMIN_LEVEL_INDENT = 50


admin.site.register(ProductMedia)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
