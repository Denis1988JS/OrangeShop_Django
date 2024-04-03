from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max, Sum

from products.models import Product

class CartQueryset(models.QuerySet):
    #Получить общую цену за товары в корзине
    def total_price(self):
        return sum(cart.get_product_price() for cart in self)

    #Получить НДС
    def total_NDS(self):
        s = float(sum(cart.get_product_price() for cart in self))
        nds = ((s/1.2) - s)*-1
        return round(nds, 2)


# Create your models here.
#Модель корзина пользователя
class UserCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    session_key = models.CharField(max_length=32, null=True, blank=True,verbose_name='Ключ сессии')

    class Meta:
        verbose_name = 'Корзина пользователя'
        verbose_name_plural = 'Корзины пользователей'

    objects = CartQueryset().as_manager()#Менеджер для корзины покупок

    #Получить сумму за товар или сумму товар если есть акция на товар:
    def get_product_price(self):
        return round(self.product.sell_price() * self.quantity, 0)

    def __str__(self):
        return f'Корзина пользователя - {self.user}'


#Модель промо-код на скидку
class PromoCode(models.Model):
    code_value = models.CharField(max_length=13, unique=True, null=False, blank=False, verbose_name='Промо-код')
    value_discont = models.SmallIntegerField(verbose_name='% скидки по промо-коду')
    create_code = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания промокода')
    activate_code = models.DateTimeField(auto_now=True,verbose_name='Дата активации промокода')
    user_cart_id = models.ForeignKey(UserCart, on_delete=models.CASCADE, verbose_name='Корзина покупок')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    is_active = models.BooleanField(default=True, verbose_name='Статус действия промокода')
    class Meta:
        verbose_name = 'Промо-код на скидку'
        verbose_name_plural = 'Промо-коды на скидку'

    def __str__(self):
        return f'Промокод - {self.code_value} на - {self.value_discont} %'
