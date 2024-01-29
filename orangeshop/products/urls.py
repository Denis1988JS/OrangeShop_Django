from django.contrib import admin
from django.urls import path, include, re_path

from products.views import CatalogProducts

urlpatterns = [
    path('',CatalogProducts.as_view(), name='catalog'),#Главная страница
]