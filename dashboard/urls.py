from django.urls import path, include
from dashboard.views import (
    ProductList,
    ProductCreate,
    load_product_type_attribute_input,
    ProductUpdate,
    ProductDetail,
    CollectionList,
    CollectionCreate,
    CollectionDetail,
    CollectionUpdate,
    ItemCreate,
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
        ProductUpdate.as_view(),
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
    path("collections/", CollectionList.as_view(), name="collection_list"),
    path(
        "collection/create/",
        CollectionCreate.as_view(),
        name="collection_create",
    ),
    path(
        "collection/detail/<int:pk>/",
        CollectionDetail.as_view(),
        name="collection_detail",
    ),
    path(
        "collection/edit/<int:pk>/",
        CollectionUpdate.as_view(),
        name="collection_edit",
    ),
    path(
        "collection/<int:pk>/item/create/",
        ItemCreate.as_view(),
        name="item_create",
    ),
]
