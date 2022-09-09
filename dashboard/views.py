from django.shortcuts import render

# Create your views here.
from django.views import View


class ProductList(View):
    def get(self, request):
        context = {}
        return render(request, "dashboard/product_list.html", context)
