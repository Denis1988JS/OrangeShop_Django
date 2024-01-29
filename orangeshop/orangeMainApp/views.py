from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView,View
from django.shortcuts import render, redirect

# Create your views here.

#Классовый шаблон - главная страница
class Homepage(TemplateView):
    template_name = 'orangeMainApp/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Магазин сантехники Orange"
        return context

