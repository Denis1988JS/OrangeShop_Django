import uuid
from django.contrib.auth.models import  User
from django.db import models
from django.urls import reverse
# Create your models here.

#Модель данные о покупателе - привязка к UserBuyers через OneToOne
class UserBuyersData(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, verbose_name='Пользователь')
    nick_name = models.CharField(max_length=50,  blank=True, null=True, verbose_name='Nick_name пользователя')
    image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Аватар')
    phone_number = models.CharField(max_length=13, blank=True, null=True, verbose_name='Номер телефона')

    class Meta:
        verbose_name = 'Данные о пользователе'
        verbose_name_plural = 'Данные о пользователях'

    def __str__(self):
        return  f'{self.nick_name} доп данные '