from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from product.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin


class ProductList(ListView):
    model = Product
    template_name = "dashboard/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        qs = Product.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    fields = [
        "product_type",
        "product_category",
        "name",
        "main_image",
        "slug",
        "description",
    ]
    template_name = "dashboard/product_create.html"
    success_url = reverse_lazy("product_list")
    success_message = "Your product create successfully"

    def form_valid(self, form):

        self.object = form.save(commit=False)

        self.object.save()

        title = self.request.POST.get("community_title")

        return super().form_valid(form)
