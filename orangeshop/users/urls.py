from django.contrib import admin
from django.urls import path, include, re_path

from users.views import RegisterUser, LoginUser

urlpatterns = [
    path('registration/', RegisterUser.as_view(), name='registration'),#Регистрация
    path('login/', LoginUser.as_view(), name='login'),#Авторизация

]