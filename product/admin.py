from django.contrib import admin
from product.models import ProductCategory, ProductMedia, ProductType, Product

admin.site.register(ProductMedia)
admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(ProductCategory)
