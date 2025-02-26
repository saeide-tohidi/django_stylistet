# Generated by Django 4.1 on 2022-09-10 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attribute", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attribute",
            name="input_type",
            field=models.CharField(
                choices=[
                    ("oneselect", "One select"),
                    ("multiselect", "Multi Select"),
                    ("numeric", "Numeric"),
                    ("boolean", "Boolean"),
                ],
                default="oneselect",
                max_length=50,
            ),
        ),
    ]
