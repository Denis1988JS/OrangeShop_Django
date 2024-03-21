from django.contrib import admin
from django.urls import path, include, re_path

from users.views import RegisterUser, LoginUser, NewPassword, UserProfile, EditUserProfile

urlpatterns = [
    path('registration/', RegisterUser.as_view(), name='registration'),#Регистрация
    path('login/', LoginUser.as_view(), name='login'),#Авторизация
    path('new_pass/', NewPassword.as_view(), name='new_pass'),#Востановить пароль
    path('user_profile/',UserProfile.as_view(), name='profile'),#Личный кабинет пользователя
    path('edit_user/<int:pk>',EditUserProfile.as_view(), name='edit_user'),#Страница редактирования пользовател
]