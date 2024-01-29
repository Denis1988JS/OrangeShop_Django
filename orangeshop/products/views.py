from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView,View
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from products.models import Product


# Create your views here.


#Классовй шаблон - каталог товаров
class CatalogProducts(ListView):
    model = Product
    template_name = 'products/catalog.html'
    context_object_name = 'products'
    paginate_by = 8
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['page_name'] = 'Товары'
        return context