from django.contrib import admin
from django.urls import path, include, re_path

from orders.views import MakeOrder

urlpatterns = [
    path('',MakeOrder.as_view(), name='makeOrder'),#Страница оформить заказ
]