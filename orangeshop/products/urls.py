from django.contrib import admin
from django.urls import path, include, re_path

from products.views import CatalogProducts, CatalogProductsCategory, SortCatalogProductsCategory

urlpatterns = [
    path('',CatalogProducts.as_view(), name='catalog'),#Страница
    path('sorted/', SortCatalogProductsCategory.as_view(), name='sorted'),#Страница с сортировкой
    path('<slug:category_slug>/',CatalogProductsCategory.as_view(), name='category'),#Страница товары по категори

]