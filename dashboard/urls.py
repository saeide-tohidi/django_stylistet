from django.urls import path, include
from dashboard.views import (
    ProductList,
)

urlpatterns = [
    # path("header", Header.as_view(), name="header"),
    # path("footer", Footer.as_view(), name="footer"),
    path("products/", ProductList.as_view(), name="product_list"),
]
