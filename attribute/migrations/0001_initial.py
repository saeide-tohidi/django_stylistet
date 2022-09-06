# Generated by Django 4.1 on 2022-09-06 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AssignedProductAttribute",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Attribute",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(allow_unicode=True, max_length=250, unique=True),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "input_type",
                    models.CharField(
                        choices=[
                            ("dropdown", "Dropdown"),
                            ("multiselect", "Multi Select"),
                            ("file", "File"),
                            ("numeric", "Numeric"),
                            ("plain-text", "Plain Text"),
                            ("boolean", "Boolean"),
                        ],
                        default="dropdown",
                        max_length=50,
                    ),
                ),
                ("value_required", models.BooleanField(blank=True, default=False)),
                (
                    "visible_in_storefront",
                    models.BooleanField(blank=True, default=True),
                ),
                (
                    "filterable_in_storefront",
                    models.BooleanField(blank=True, default=False),
                ),
                (
                    "filterable_in_dashboard",
                    models.BooleanField(blank=True, default=False),
                ),
                (
                    "storefront_search_position",
                    models.IntegerField(blank=True, default=0),
                ),
                ("available_in_grid", models.BooleanField(blank=True, default=False)),
            ],
            options={
                "ordering": ("slug",),
            },
        ),
        migrations.CreateModel(
            name="AttributeValue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250)),
                ("picture", models.ImageField(blank=True, null=True, upload_to="")),
                ("value", models.CharField(blank=True, default="", max_length=100)),
                ("slug", models.SlugField(allow_unicode=True, max_length=255)),
                ("file_url", models.URLField(blank=True, null=True)),
                (
                    "content_type",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("plain_text", models.TextField(blank=True, null=True)),
                ("boolean", models.BooleanField(blank=True, null=True)),
                ("date_time", models.DateTimeField(blank=True, null=True)),
                (
                    "attribute",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="values",
                        to="attribute.attribute",
                    ),
                ),
            ],
            options={
                "ordering": ("pk",),
                "unique_together": {("slug", "attribute")},
            },
        ),
        migrations.CreateModel(
            name="AttributeProduct",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "assigned_products",
                    models.ManyToManyField(
                        blank=True,
                        related_name="attributesrelated",
                        through="attribute.AssignedProductAttribute",
                        to="product.product",
                    ),
                ),
                (
                    "attribute",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attributeproduct",
                        to="attribute.attribute",
                    ),
                ),
                (
                    "product_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attributeproduct",
                        to="product.producttype",
                    ),
                ),
            ],
            options={
                "ordering": ("pk",),
                "unique_together": {("attribute", "product_type")},
            },
        ),
        migrations.AddField(
            model_name="attribute",
            name="product_types",
            field=models.ManyToManyField(
                blank=True,
                related_name="product_attributes",
                through="attribute.AttributeProduct",
                to="product.producttype",
            ),
        ),
        migrations.CreateModel(
            name="AssignedProductAttributeValue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "assignment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="productvalueassignment",
                        to="attribute.assignedproductattribute",
                    ),
                ),
                (
                    "value",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="productvalueassignment",
                        to="attribute.attributevalue",
                    ),
                ),
            ],
            options={
                "ordering": ("pk",),
                "unique_together": {("value", "assignment")},
            },
        ),
        migrations.AddField(
            model_name="assignedproductattribute",
            name="assignment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="productassignments",
                to="attribute.attributeproduct",
            ),
        ),
        migrations.AddField(
            model_name="assignedproductattribute",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attributes",
                to="product.product",
            ),
        ),
        migrations.AddField(
            model_name="assignedproductattribute",
            name="values",
            field=models.ManyToManyField(
                blank=True,
                related_name="productassignments",
                through="attribute.AssignedProductAttributeValue",
                to="attribute.attributevalue",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="assignedproductattribute",
            unique_together={("product", "assignment")},
        ),
    ]
