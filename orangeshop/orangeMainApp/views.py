from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView,View
from django.shortcuts import render, redirect

from carts.templates.utils import CartSumMixin


# Create your views here.

#Классовый шаблон - главная страница
class Homepage(CartSumMixin,TemplateView):
    template_name = 'orangeMainApp/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        context['title'] = "Магазин сантехники Orange"
        context = dict(list(context.items()) + list(c_def.items()))
        return context

