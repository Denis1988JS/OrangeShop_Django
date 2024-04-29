from django.contrib import admin
from django.urls import path, include, re_path

from orders.views import MakeOrder, AddOrder

urlpatterns = [
    path('',MakeOrder.as_view(), name='makeOrder'),#Страница оформить заказ
    path('addOrder', AddOrder.as_view(), name='addOrder'),#Страница обработчик формы оформления заказа
]