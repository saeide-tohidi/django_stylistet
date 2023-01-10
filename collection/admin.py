from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from collection.models import (
    Collection,
    CollectionAttribute,
    CollectionAttributeValue,
    AssignedCollectionAttribute,
    AssignedCollectionAttributeValue,
    AssignedItemAttribute,
    AssignedItemAttributeValue,
    Item,
)


class CollectionAttributeValueInline(admin.StackedInline):
    model = CollectionAttributeValue
    readonly_fields = ["slug", "value"]


class CollectionAttributeAdmin(ImportExportModelAdmin):
    model = CollectionAttribute
    fields = [
        "name",
        "input_type",
        "image_value",
        "value_required",
        "slug",
    ]
    list_display = [
        "name",
        "input_type",
        "image_value",
        "value_required",
        "get_values_list",
        "get_values_count",
    ]
    readonly_fields = [
        "get_values_count",
        "get_values_list",
        "slug",
    ]
    inlines = [
        CollectionAttributeValueInline,
    ]

    def get_values_count(self, obj):
        return obj.values.count()

    get_values_count.allow_tags = True
    get_values_count.short_description = "All values count"

    def get_values_list(self, obj):
        val_list = []
        for val in obj.values.all():
            val_list.append(val.name)
        return val_list

    get_values_list.allow_tags = True
    get_values_list.short_description = "All values name"


admin.site.register(Collection)
admin.site.register(CollectionAttribute, CollectionAttributeAdmin)
admin.site.register(CollectionAttributeValue)
admin.site.register(AssignedCollectionAttribute)
admin.site.register(AssignedCollectionAttributeValue)
admin.site.register(AssignedItemAttribute)
admin.site.register(AssignedItemAttributeValue)
admin.site.register(Item)
