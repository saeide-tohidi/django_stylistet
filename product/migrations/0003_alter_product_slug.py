# Generated by Django 4.1 on 2022-09-13 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0002_product_main_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=models.SlugField(
                allow_unicode=True, blank=True, max_length=255, unique=True
            ),
        ),
    ]
