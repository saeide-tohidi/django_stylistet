from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from collection.api.views import (
    CollectionListAPIViewSet,
    CollectionDetailAPIView,
    ItemDetailAPIView,
)

urlpatterns = [
    path(
        "v1/collection/list",
        CollectionListAPIViewSet.as_view(),
        name="collection_list_api",
    ),
    path(
        "v1/collection/<int:pk>/",
        CollectionDetailAPIView.as_view(),
        name="collection_detail_api",
    ),
    path("v1/item/<int:pk>/", ItemDetailAPIView.as_view(), name="item_detail_api"),
]
