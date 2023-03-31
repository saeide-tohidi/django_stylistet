from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from rest_framework import generics, permissions
from django_filters import rest_framework as filters
from collection.api.serializers import (
    CollectionListSerializer,
    CollectionDetailSerializer,
    ItemSerializerLink,
)
from collection.models import Collection, Item


class CollectionListAPIViewSet(generics.ListAPIView):
    serializer_class = CollectionListSerializer
    queryset = Collection.objects.all()


class CollectionDetailAPIView(generics.RetrieveAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionDetailSerializer

    def get(self, request, *args, **kwargs):
        collection = self.get_object()
        serializer = self.get_serializer(collection)
        return Response(serializer.data)


class ItemDetailAPIView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializerLink

    def get(self, request, *args, **kwargs):
        item = self.get_object()
        serializer = self.get_serializer(item)
        return Response(serializer.data)
