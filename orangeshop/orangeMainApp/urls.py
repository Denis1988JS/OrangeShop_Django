from django.contrib import admin
from django.urls import path, include, re_path

from orangeMainApp.views import Homepage

urlpatterns = [
    path('',Homepage.as_view(), name='home'),#Главная страница
]