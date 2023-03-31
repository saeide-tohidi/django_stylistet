from rest_framework import serializers

from collection.models import Collection, Item


class CollectionListSerializer(serializers.ModelSerializer):
    collection_url = serializers.HyperlinkedIdentityField(
        view_name="collection_detail_api"
    )

    class Meta:
        model = Collection
        fields = [
            "collection_url",
            "name",
        ]


class ItemSerializerLink(serializers.ModelSerializer):
    item_url = serializers.HyperlinkedIdentityField(view_name="item_detail_api")

    class Meta:
        model = Item
        fields = [
            "name",
            "item_url",
        ]


class CollectionDetailSerializer(serializers.ModelSerializer):
    item_set = ItemSerializerLink(source="items", many=True, read_only=True)

    class Meta:
        model = Collection
        fields = [
            "id",
            "name",
            "main_image",
            "description",
            "created_at",
            "updated_at",
            "item_set",
            "slug",
        ]
