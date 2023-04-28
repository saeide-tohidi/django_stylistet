from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView, DetailView

from collection.filter import ItemProductsFilter
from collection.models import (
    Collection,
    CollectionAttribute,
    AssignedCollectionAttribute,
    AssignedCollectionAttributeValue,
    CollectionAttributeValue,
    Item,
    AssignedItemAttribute,
    AssignedItemAttributeValue,
)
from product.models import Product, ProductType, ProductCategory, create_currency
from django.db import transaction
from braces.views import StaffuserRequiredMixin
from attribute.models import (
    Attribute,
    AttributeProduct,
    AssignedProductAttribute,
    AssignedProductAttributeValue,
    AttributeValue,
)
from babel.numbers import list_currencies


class ProductList(StaffuserRequiredMixin, ListView):
    model = Product
    template_name = "dashboard/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        qs = Product.objects.all().order_by("-id")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductDetail(StaffuserRequiredMixin, SuccessMessageMixin, DetailView):
    template_name = "dashboard/product_detail.html"
    model = Product
    context_object_name = "product"
    pk_url_kwarg = "pk"
    query_pk_and_slug = True

    def get_queryset(self):
        return Product.objects.filter()

    def get(self, request, pk):
        return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        attributes = Attribute.objects.filter(product_types=product.product_type.id)
        booleans = attributes.filter(input_type="boolean")
        oneselect_with_pic = attributes.filter(input_type="oneselect", image_value=True)
        oneselect_no_pic = attributes.filter(input_type="oneselect", image_value=False)
        multiselect_with_pic = attributes.filter(
            input_type="multiselect", image_value=True
        )
        multiselect_no_pic = attributes.filter(
            input_type="multiselect", image_value=False
        )
        context["booleans"] = booleans
        context["oneselect_with_pic"] = oneselect_with_pic
        context["oneselect_no_pic"] = oneselect_no_pic
        context["multiselect_with_pic"] = multiselect_with_pic
        context["multiselect_no_pic"] = multiselect_no_pic
        context["product_type"] = ProductType.objects.all()
        context["product_category"] = ProductCategory.objects.all()
        context["all_values"] = AssignedProductAttributeValue.objects.filter(
            assignment__product=self.object
        ).values_list("value_id", flat=True)
        context["currency"] = list_currencies()
        return context


class ProductCreate(StaffuserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    fields = [
        "product_type",
        "product_category",
        "name",
        "main_image",
        "description",
        "price_amount",
        "currency",
        "shopping_url",
    ]
    template_name = "dashboard/product_create.html"
    success_url = reverse_lazy("product_list")
    success_message = "Your product create successfully"

    def form_valid(self, form):

        with transaction.atomic():

            self.object = form.save(commit=False)
            product_type = self.request.POST.get("product_type")
            attributes = AttributeProduct.objects.filter(product_type_id=product_type)
            self.object.save()
            self.success_url = reverse_lazy(
                "product_detail", kwargs={"pk": self.object.pk}
            )
            for attr in attributes:
                if self.request.POST.get(attr.attribute.slug):
                    attr_values = self.request.POST.get(attr.attribute.slug)
                    if attr.attribute.input_type == "oneselect":
                        value = AttributeValue.objects.filter(id=attr_values).first()
                        attr_product = AssignedProductAttribute()
                        attr_product.product = self.object
                        attr_product.assignment = attr
                        attr_product.save()
                        attr_product_value = AssignedProductAttributeValue()
                        attr_product_value.assignment = attr_product
                        attr_product_value.value = value
                        attr_product_value.save()

                    if attr.attribute.input_type == "multiselect":
                        attr_values = self.request.POST.getlist(attr.attribute.slug)
                        attr_product = AssignedProductAttribute()
                        attr_product.product = self.object
                        attr_product.assignment = attr
                        attr_product.save()
                        for val in attr_values:
                            val = AttributeValue.objects.filter(id=val).first()
                            attr_product_value = AssignedProductAttributeValue()
                            attr_product_value.assignment = attr_product
                            attr_product_value.value = val
                            attr_product_value.save()

                    if attr.attribute.input_type == "boolean":
                        value = AttributeValue.objects.filter(id=attr_values).first()
                        attr_product = AssignedProductAttribute()
                        attr_product.product = self.object
                        attr_product.assignment = attr
                        attr_product.save()
                        attr_product_value = AssignedProductAttributeValue()
                        attr_product_value.assignment = attr_product
                        attr_product_value.value = value
                        attr_product_value.save()

            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_type"] = ProductType.objects.all()
        context["product_category"] = ProductCategory.objects.all()
        context["currency"] = list_currencies()
        return context


class ProductUpdate(StaffuserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    fields = [
        "product_category",
        "name",
        "main_image",
        "description",
        "price_amount",
        "currency",
        "shopping_url",
    ]
    template_name = "dashboard/product_detail.html"
    success_url = reverse_lazy("product_list")
    success_message = "Your product updated successfully"
    pk_url_kwarg = "pk"
    query_pk_and_slug = True

    def get_queryset(self):
        return Product.objects.filter()

    def form_valid(self, form):

        with transaction.atomic():
            self.object = form.save(commit=False)
            self.success_url = reverse_lazy(
                "product_detail", kwargs={"pk": self.object.pk}
            )
            product_type = ProductType.objects.get(
                id=self.request.POST.get("product_type")
            )
            attributes = AttributeProduct.objects.filter(product_type=product_type)

            # if change product type:
            if self.object.product_type != product_type:
                per_assigned = AssignedProductAttribute.objects.filter(
                    product=self.object
                )
                for assigned in per_assigned:
                    assigned.delete()
                product_type = ProductType.objects.get(
                    id=self.request.POST.get("product_type")
                )
                self.object.product_type = product_type
                self.object.save()
                for attr in attributes:
                    if self.request.POST.get(attr.attribute.slug):
                        attr_values = self.request.POST.get(attr.attribute.slug)
                        if attr.attribute.input_type == "oneselect":
                            value = AttributeValue.objects.filter(
                                id=attr_values
                            ).first()
                            attr_product = AssignedProductAttribute()
                            attr_product.product = self.object
                            attr_product.assignment = attr
                            attr_product.save()
                            attr_product_value = AssignedProductAttributeValue()
                            attr_product_value.assignment = attr_product
                            attr_product_value.value = value
                            attr_product_value.save()

                        if attr.attribute.input_type == "multiselect":
                            attr_values = self.request.POST.getlist(attr.attribute.slug)
                            attr_product = AssignedProductAttribute()
                            attr_product.product = self.object
                            attr_product.assignment = attr
                            attr_product.save()
                            for val in attr_values:
                                val = AttributeValue.objects.filter(id=val).first()
                                attr_product_value = AssignedProductAttributeValue()
                                attr_product_value.assignment = attr_product
                                attr_product_value.value = val
                                attr_product_value.save()

                        if attr.attribute.input_type == "boolean":
                            value = AttributeValue.objects.filter(
                                id=attr_values
                            ).first()
                            attr_product = AssignedProductAttribute()
                            attr_product.product = self.object
                            attr_product.assignment = attr
                            attr_product.save()
                            attr_product_value = AssignedProductAttributeValue()
                            attr_product_value.assignment = attr_product
                            attr_product_value.value = value
                            attr_product_value.save()
            else:
                for attr in attributes:
                    if self.request.POST.get(attr.attribute.slug):
                        attr_values = self.request.POST.get(attr.attribute.slug)
                        if attr.attribute.input_type == "oneselect":
                            value = AttributeValue.objects.filter(
                                id=attr_values
                            ).first()
                            (
                                attr_product,
                                create,
                            ) = AssignedProductAttribute.objects.get_or_create(
                                product=self.object, assignment=attr
                            )
                            (
                                attr_product_value,
                                create,
                            ) = AssignedProductAttributeValue.objects.get_or_create(
                                assignment=attr_product, value=value
                            )
                            previous_values = (
                                AssignedProductAttributeValue.objects.filter(
                                    assignment=attr_product
                                ).exclude(id=attr_product_value.id)
                            )
                            for val in previous_values:
                                val.delete()

                        if attr.attribute.input_type == "multiselect":
                            attr_values = self.request.POST.getlist(attr.attribute.slug)
                            (
                                attr_product,
                                create,
                            ) = AssignedProductAttribute.objects.get_or_create(
                                product=self.object, assignment=attr
                            )
                            previous_values = (
                                AssignedProductAttributeValue.objects.filter(
                                    assignment=attr_product
                                )
                            )
                            for val in attr_values:
                                val = AttributeValue.objects.filter(id=val).first()
                                (
                                    attr_product_value,
                                    create,
                                ) = AssignedProductAttributeValue.objects.get_or_create(
                                    assignment=attr_product, value=val
                                )
                                previous_values = previous_values.exclude(
                                    id=attr_product_value.id
                                )
                            for val in previous_values:
                                val.delete()

                        if attr.attribute.input_type == "boolean":
                            value = AttributeValue.objects.filter(
                                id=attr_values
                            ).first()
                            (
                                attr_product,
                                create,
                            ) = AssignedProductAttribute.objects.get_or_create(
                                product=self.object, assignment=attr
                            )
                            AssignedProductAttributeValue.objects.get_or_create(
                                assignment=attr_product, value=value
                            )
                    else:
                        attr_product = AssignedProductAttribute.objects.filter(
                            product=self.object, assignment=attr
                        )
                        for at in attr_product:
                            at.delete()

            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context["product_type"] = ProductType.objects.all()
        context["product_category"] = ProductCategory.objects.all()
        attributes = Attribute.objects.filter(product_types=product.product_type.id)
        booleans = attributes.filter(input_type="boolean")
        oneselect_with_pic = attributes.filter(input_type="oneselect", image_value=True)
        oneselect_no_pic = attributes.filter(input_type="oneselect", image_value=False)
        multiselect_with_pic = attributes.filter(
            input_type="multiselect", image_value=True
        )
        multiselect_no_pic = attributes.filter(
            input_type="multiselect", image_value=False
        )
        context["booleans"] = booleans
        context["oneselect_with_pic"] = oneselect_with_pic
        context["oneselect_no_pic"] = oneselect_no_pic
        context["multiselect_with_pic"] = multiselect_with_pic
        context["multiselect_no_pic"] = multiselect_no_pic
        context["product_type"] = ProductType.objects.all()
        context["product_category"] = ProductCategory.objects.all()
        context["all_values"] = AssignedProductAttributeValue.objects.filter(
            assignment__product=self.object
        ).values_list("value_id", flat=True)
        context["currency"] = list_currencies()
        return context


def load_product_type_attribute_input(request):
    if "product_type_id" in request.GET:
        product_type_id = request.GET.get("product_type_id")
        attributes = Attribute.objects.filter(product_types=product_type_id)
        booleans = attributes.filter(input_type="boolean")
        oneselect_with_pic = attributes.filter(input_type="oneselect", image_value=True)
        oneselect_no_pic = attributes.filter(input_type="oneselect", image_value=False)
        multiselect_with_pic = attributes.filter(
            input_type="multiselect", image_value=True
        )
        multiselect_no_pic = attributes.filter(
            input_type="multiselect", image_value=False
        )
        all_values = []
        if "product_id" in request.GET:
            product_id = request.GET.get("product_id")
            product = Product.objects.get(id=product_id)
            all_values = AssignedProductAttributeValue.objects.filter(
                assignment__product=product
            ).values_list("value_id", flat=True)

        context = {
            "booleans": booleans,
            "oneselect_with_pic": oneselect_with_pic,
            "oneselect_no_pic": oneselect_no_pic,
            "multiselect_with_pic": multiselect_with_pic,
            "multiselect_no_pic": multiselect_no_pic,
            "all_values": all_values,
        }
        return render(request, "dashboard/attribute_input.html", context)


class CollectionList(StaffuserRequiredMixin, ListView):
    model = Collection
    template_name = "dashboard/collection_list.html"
    context_object_name = "collections"

    def get_queryset(self):
        qs = Collection.objects.all().order_by("-id")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CollectionCreate(StaffuserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Collection
    fields = [
        "name",
        "main_image",
        "description",
    ]
    template_name = "dashboard/collection_create.html"
    success_url = reverse_lazy("collection_list")
    success_message = "Your collection created successfully"

    def form_valid(self, form):
        test = self.request.POST
        print(test)
        with transaction.atomic():

            self.object = form.save(commit=False)
            attributes = CollectionAttribute.objects.all()
            self.object.save()
            self.success_url = reverse_lazy(
                "product_detail", kwargs={"pk": self.object.pk}
            )
            for attr in attributes:
                print(attr)
                if self.request.POST.get(attr.slug):
                    attr_values = self.request.POST.get(attr.slug)
                    if attr.input_type == "oneselect":
                        value = CollectionAttributeValue.objects.filter(
                            id=attr_values
                        ).first()
                        attr_product = AssignedCollectionAttribute()
                        attr_product.collection = self.object
                        attr_product.attribute = attr
                        attr_product.save()
                        attr_product_value = AssignedCollectionAttributeValue()
                        attr_product_value.assignment = attr_product
                        attr_product_value.value = value
                        attr_product_value.save()

                    if attr.input_type == "multiselect":
                        attr_values = self.request.POST.getlist(attr.slug)
                        attr_product = AssignedCollectionAttribute()
                        attr_product.collection = self.object
                        attr_product.attribute = attr
                        attr_product.save()
                        for val in attr_values:
                            val = CollectionAttributeValue.objects.filter(
                                id=val
                            ).first()
                            attr_product_value = AssignedCollectionAttributeValue()
                            attr_product_value.assignment = attr_product
                            attr_product_value.value = val
                            attr_product_value.save()

                    if attr.input_type == "boolean":
                        value = CollectionAttributeValue.objects.filter(
                            id=attr_values
                        ).first()
                        attr_product = AssignedCollectionAttribute()
                        attr_product.product = self.object
                        attr_product.attribute = attr
                        attr_product.save()
                        attr_product_value = AssignedCollectionAttributeValue()
                        attr_product_value.assignment = attr_product
                        attr_product_value.value = value
                        attr_product_value.save()

            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attributes = CollectionAttribute.objects.all()
        booleans = attributes.filter(input_type="boolean")
        oneselect_with_pic = attributes.filter(input_type="oneselect", image_value=True)
        oneselect_no_pic = attributes.filter(input_type="oneselect", image_value=False)
        multiselect_with_pic = attributes.filter(
            input_type="multiselect", image_value=True
        )
        multiselect_no_pic = attributes.filter(
            input_type="multiselect", image_value=False
        )
        context["booleans"] = booleans
        context["oneselect_with_pic"] = oneselect_with_pic
        context["oneselect_no_pic"] = oneselect_no_pic
        context["multiselect_with_pic"] = multiselect_with_pic
        context["multiselect_no_pic"] = multiselect_no_pic

        return context


class CollectionDetail(StaffuserRequiredMixin, SuccessMessageMixin, DetailView):
    template_name = "dashboard/collection_detail.html"
    model = Collection
    context_object_name = "collection"
    pk_url_kwarg = "pk"
    query_pk_and_slug = True

    def get_queryset(self):
        return Collection.objects.filter()

    def get(self, request, pk):
        return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection = self.object
        print(collection)
        attributes = CollectionAttribute.objects.all()
        booleans = attributes.filter(input_type="boolean")
        oneselect_with_pic = attributes.filter(input_type="oneselect", image_value=True)
        oneselect_no_pic = attributes.filter(input_type="oneselect", image_value=False)
        multiselect_with_pic = attributes.filter(
            input_type="multiselect", image_value=True
        )
        multiselect_no_pic = attributes.filter(
            input_type="multiselect", image_value=False
        )
        context["booleans"] = booleans
        context["oneselect_with_pic"] = oneselect_with_pic
        context["oneselect_no_pic"] = oneselect_no_pic
        context["multiselect_with_pic"] = multiselect_with_pic
        context["multiselect_no_pic"] = multiselect_no_pic
        context["all_values"] = AssignedCollectionAttributeValue.objects.filter(
            assignment__collection=self.object
        ).values_list("value_id", flat=True)

        context["product_type"] = ProductType.objects.all()

        return context


class CollectionUpdate(StaffuserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Collection
    fields = [
        "name",
        "main_image",
        "description",
    ]
    template_name = "dashboard/collection_detail.html"
    success_url = reverse_lazy("collection_detail")
    success_message = "Your collection updated successfully"
    pk_url_kwarg = "pk"
    query_pk_and_slug = True

    def get_queryset(self):
        return Collection.objects.filter()

    def form_valid(self, form):
        self.success_url = reverse_lazy(
            "collection_detail", kwargs={"pk": self.object.pk}
        )
        with transaction.atomic():
            self.object = form.save(commit=False)
            attributes = CollectionAttribute.objects.all()
            for attr in attributes:
                if self.request.POST.get(attr.slug):
                    attr_values = self.request.POST.get(attr.slug)
                    if attr.input_type == "oneselect":
                        value = CollectionAttributeValue.objects.filter(
                            id=attr_values
                        ).first()
                        (
                            attr_product,
                            create,
                        ) = AssignedCollectionAttribute.objects.get_or_create(
                            collection=self.object, attribute=attr
                        )
                        (
                            attr_product_value,
                            create,
                        ) = AssignedCollectionAttributeValue.objects.get_or_create(
                            assignment=attr_product, value=value
                        )
                        previous_values = (
                            AssignedCollectionAttributeValue.objects.filter(
                                assignment=attr_product
                            ).exclude(id=attr_product_value.id)
                        )
                        for val in previous_values:
                            val.delete()

                    if attr.input_type == "multiselect":
                        attr_values = self.request.POST.getlist(attr.slug)
                        (
                            attr_product,
                            create,
                        ) = AssignedCollectionAttribute.objects.get_or_create(
                            collection=self.object, attribute=attr
                        )
                        previous_values = (
                            AssignedCollectionAttributeValue.objects.filter(
                                assignment=attr_product
                            )
                        )
                        for val in attr_values:
                            val = CollectionAttributeValue.objects.filter(
                                id=val
                            ).first()
                            (
                                attr_product_value,
                                create,
                            ) = AssignedCollectionAttributeValue.objects.get_or_create(
                                assignment=attr_product, value=val
                            )
                            previous_values = previous_values.exclude(
                                id=attr_product_value.id
                            )
                        for val in previous_values:
                            val.delete()

                    if attr.input_type == "boolean":
                        value = CollectionAttributeValue.objects.filter(
                            id=attr_values
                        ).first()
                        (
                            attr_product,
                            create,
                        ) = AssignedCollectionAttribute.objects.get_or_create(
                            collection=self.object, attribute=attr
                        )
                        AssignedCollectionAttributeValue.objects.get_or_create(
                            assignment=attr_product, value=value
                        )
                else:
                    attr_product = AssignedCollectionAttribute.objects.filter(
                        collection=self.object, attribute=attr
                    )
                    for at in attr_product:
                        at.delete()

        return super().form_valid(form)


class ItemCreate(StaffuserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Item
    fields = [
        "name",
        "collection",
        "product_type",
    ]
    template_name = "dashboard/collection_item_create.html"
    success_url = reverse_lazy("product_list")
    success_message = "Your product create successfully"

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            product_type = self.request.POST.get("product_type")
            attributes = AttributeProduct.objects.filter(product_type_id=product_type)
            self.object.save()
            self.success_url = reverse_lazy(
                "collection_detail", kwargs={"pk": self.object.collection.pk}
            )
            for attr in attributes:
                if self.request.POST.get(attr.attribute.slug):
                    attr_values = self.request.POST.get(attr.attribute.slug)
                    if attr.attribute.input_type == "oneselect":
                        value = AttributeValue.objects.filter(id=attr_values).first()
                        attr_product = AssignedItemAttribute()
                        attr_product.item = self.object
                        attr_product.assignment = attr
                        attr_product.save()
                        attr_product_value = AssignedItemAttributeValue()
                        attr_product_value.assignment = attr_product
                        attr_product_value.value = value
                        attr_product_value.save()

                    if attr.attribute.input_type == "multiselect":
                        attr_values = self.request.POST.getlist(attr.attribute.slug)
                        attr_product = AssignedItemAttribute()
                        attr_product.item = self.object
                        attr_product.assignment = attr
                        attr_product.save()
                        for val in attr_values:
                            val = AttributeValue.objects.filter(id=val).first()
                            attr_product_value = AssignedItemAttributeValue()
                            attr_product_value.assignment = attr_product
                            attr_product_value.value = val
                            attr_product_value.save()

                    if attr.attribute.input_type == "boolean":
                        value = AttributeValue.objects.filter(id=attr_values).first()
                        attr_product = AssignedItemAttribute()
                        attr_product.item = self.object
                        attr_product.assignment = attr
                        attr_product.save()
                        attr_product_value = AssignedItemAttributeValue()
                        attr_product_value.assignment = attr_product
                        attr_product_value.value = value
                        attr_product_value.save()

            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["collection"] = self.kwargs.get("pk")
        context["product_type"] = ProductType.objects.all()
        return context


class ItemDetail(StaffuserRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "dashboard/collection_item_detail.html"
    model = Item
    context_object_name = "product"
    pk_url_kwarg = "pk"
    query_pk_and_slug = True
    fields = [
        "name",
    ]

    def get_queryset(self):
        return Item.objects.filter()

    def get(self, request, pk):
        return super().get(request)

    def form_valid(self, form):

        with transaction.atomic():
            self.object = form.save(commit=False)
            self.success_url = reverse_lazy(
                "item_detail", kwargs={"pk": self.object.pk}
            )
            attributes = AttributeProduct.objects.filter(
                product_type=self.object.product_type
            )

            for attr in attributes:
                if self.request.POST.get(attr.attribute.slug):
                    attr_values = self.request.POST.get(attr.attribute.slug)
                    if attr.attribute.input_type == "oneselect":
                        value = AttributeValue.objects.filter(id=attr_values).first()
                        (
                            attr_product,
                            create,
                        ) = AssignedItemAttribute.objects.get_or_create(
                            item=self.object, assignment=attr
                        )
                        (
                            attr_product_value,
                            create,
                        ) = AssignedItemAttributeValue.objects.get_or_create(
                            assignment=attr_product, value=value
                        )
                        previous_values = AssignedItemAttributeValue.objects.filter(
                            assignment=attr_product
                        ).exclude(id=attr_product_value.id)
                        for val in previous_values:
                            val.delete()

                    if attr.attribute.input_type == "multiselect":
                        attr_values = self.request.POST.getlist(attr.attribute.slug)
                        (
                            attr_product,
                            create,
                        ) = AssignedItemAttribute.objects.get_or_create(
                            item=self.object, assignment=attr
                        )
                        previous_values = AssignedItemAttributeValue.objects.filter(
                            assignment=attr_product
                        )
                        for val in attr_values:
                            val = AttributeValue.objects.filter(id=val).first()
                            (
                                attr_product_value,
                                create,
                            ) = AssignedItemAttributeValue.objects.get_or_create(
                                assignment=attr_product, value=val
                            )
                            previous_values = previous_values.exclude(
                                id=attr_product_value.id
                            )
                        for val in previous_values:
                            val.delete()

                    if attr.attribute.input_type == "boolean":
                        value = AttributeValue.objects.filter(id=attr_values).first()
                        (
                            attr_product,
                            create,
                        ) = AssignedItemAttribute.objects.get_or_create(
                            item=self.object, assignment=attr
                        )
                        AssignedItemAttributeValue.objects.get_or_create(
                            assignment=attr_product, value=value
                        )
                else:
                    attr_product = AssignedItemAttribute.objects.filter(
                        item=self.object, assignment=attr
                    )
                    for at in attr_product:
                        at.delete()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object
        attributes = Attribute.objects.filter(product_types=item.product_type.id)
        booleans = attributes.filter(input_type="boolean")
        oneselect_with_pic = attributes.filter(input_type="oneselect", image_value=True)
        oneselect_no_pic = attributes.filter(input_type="oneselect", image_value=False)
        multiselect_with_pic = attributes.filter(
            input_type="multiselect", image_value=True
        )
        multiselect_no_pic = attributes.filter(
            input_type="multiselect", image_value=False
        )
        context["booleans"] = booleans
        context["oneselect_with_pic"] = oneselect_with_pic
        context["oneselect_no_pic"] = oneselect_no_pic
        context["multiselect_with_pic"] = multiselect_with_pic
        context["multiselect_no_pic"] = multiselect_no_pic
        context["product_type"] = ProductType.objects.all()
        context["all_values"] = AssignedItemAttributeValue.objects.filter(
            assignment__item=self.object
        ).values_list("value_id", flat=True)
        product = Product.objects.filter(product_type=item.product_type)

        for creator in item.get_attr_values_filter_dict["values_num"]:
            product = product.filter(
                attributes__productvalueassignment__value__id=creator
            )
        context["products"] = product.distinct()
        return context


class ItemDelete(View):
    def get(self, request, pk, *args, **kwargs):
        item = Item.objects.get(id=pk)
        collection_pk = item.collection.pk
        item.delete()
        messages.success(self.request, "You delete that item successfully")
        return redirect(
            to=reverse_lazy("collection_detail", kwargs={"pk": collection_pk})
        )


class CollectionDelete(View):
    def get(self, request, pk, *args, **kwargs):
        collection = Collection.objects.get(pk=pk)
        items = collection.items.all()
        for item in items:
            item.delete()
        collection.delete()
        messages.success(self.request, "You delete that collection successfully")
        return redirect(to=reverse_lazy("collection_list"))
