from django.urls import path, include
from dashboard.views import (
    ProductList,
    ProductCreate,
    load_product_type_attribute_input,
    ProductEdit,
    ProductDetail,
)

urlpatterns = [
    path("products/", ProductList.as_view(), name="product_list"),
    path(
        "product/create/",
        ProductCreate.as_view(),
        name="product_create",
    ),
    path(
        "product/edit/<int:pk>/",
        ProductEdit.as_view(),
        name="product_edit",
    ),
    path(
        "product/detail/<int:pk>/",
        ProductDetail.as_view(),
        name="product_detail",
    ),
    path(
        "ajax/load_product_type_attr_input/",
        load_product_type_attribute_input,
        name="ajax_load_product_type_attr_input",
    ),
]
