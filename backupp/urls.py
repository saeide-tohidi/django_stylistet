from django.urls import path
from .views import dump_view

urlpatterns = [
    path(
        "dump/",
        dump_view,
        name="backup_dump",
    ),
]
