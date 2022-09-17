from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify

from product.models import Product
import shortuuid


@receiver(pre_save, sender=Product)
def user_slug(sender, instance, **kwargs):
    if instance.name and instance.name not in instance.slug:
        slug = slugify(instance.name, allow_unicode=True)
        slug = slug + "-" + shortuuid.ShortUUID().random(length=5)
        instance.slug = slug
