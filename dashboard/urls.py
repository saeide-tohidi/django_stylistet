from django.urls import path, include
from dashboard.views import ProductList, ProductCreate

urlpatterns = [
    path("products/", ProductList.as_view(), name="product_list"),
    path(
        "product/create/",
        ProductCreate.as_view(),
        name="product_create",
    ),
]
