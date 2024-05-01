from django.contrib import admin
from django.urls import path, include, re_path

from orders.views import MakeOrder, AddOrder, OrderMessage, OrderDetail

urlpatterns = [
    path('',MakeOrder.as_view(), name='makeOrder'),#Страница оформить заказ
    path('addOrder/', AddOrder.as_view(), name='addOrder'),#Страница обработчик формы оформления заказа
    path('<slug:slug>/',OrderDetail.as_view(), name='orderDetail'),#Детально о заказе
    path('addOrder/orderMessage/<int:pk>', OrderMessage.as_view(), name='orderMessage'),#Сообщение о заказе

]