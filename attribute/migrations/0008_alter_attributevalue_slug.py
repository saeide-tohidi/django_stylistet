# Generated by Django 3.2.10 on 2022-11-30 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attribute", "0007_alter_attribute_input_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attributevalue",
            name="slug",
            field=models.SlugField(allow_unicode=True, blank=True, max_length=255),
        ),
    ]
