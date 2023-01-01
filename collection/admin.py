from django.contrib import admin

# Register your models here.
from collection.models import (
    Collection,
    CollectionAttribute,
    CollectionAttributeValue,
    AssignedCollectionAttribute,
    AssignedCollectionAttributeValue,
)

admin.site.register(Collection)
admin.site.register(CollectionAttribute)
admin.site.register(CollectionAttributeValue)
admin.site.register(AssignedCollectionAttribute)
admin.site.register(AssignedCollectionAttributeValue)
