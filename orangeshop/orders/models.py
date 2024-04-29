from django.contrib.auth.models import User
from django.db import models

from datetime import datetime
from random import random, randint

from products.models import Product


#Функция для номера заказа - R+ДАТА+ВРЕМЯ+случайное число от 1000 до 9999
def RandomOrderNumber():
    current_datetime = datetime.now()
    yearOrder = str(current_datetime.year)
    monthOrder = str(current_datetime.month)
    dayOrder = str(current_datetime.day)
    hourOrder = str(current_datetime.hour)
    minOrder = str(current_datetime.minute)
    x =  randint(1000, 9999)
    number = 'R' + yearOrder + monthOrder + dayOrder + hourOrder + minOrder + str(x)
    return number

# Create your models here.
#Модель статус покупателя Физлицо/Юрлицо
class BuyerStatus(models.Model):
    status = models.CharField(max_length= 20, verbose_name='Статус (заказ от имени)')
    full_status = models.CharField(max_length=50, verbose_name='Полное наименование')
    class Meta:
        verbose_name = "Статус покупателя"
        verbose_name_plural = "Статусы покупателей"
    def __str__(self):
        return f"{self.status}"

#Модель способ получения
class MethodOfObtaining(models.Model):
    method_name = models.CharField(max_length=20, verbose_name="Способ получения")
    class Meta:
        verbose_name = "Способ получения заказа"
        verbose_name_plural = "Способы получения заказов"
    def __str__(self):
        return f"Получение - {self.method_name}"

#Модель метод оплаты
class PayMethod(models.Model):
    method_name = models.CharField(max_length=20, verbose_name='Метод оплаты')
    #Формы оплаты через карту или тинькофф - будут подгружаться через jQuery - чтобы не хранить в базе данные карточек
    class Meta:
        verbose_name = "Метод оплаты заказа"
        verbose_name_plural = "Методы оплаты заказов"
    def __str__(self):
        return f"Оплата - {self.method_name}"

#Менеджер модели заказа
class OrderItemQueryset(models.QuerySet):
    #Получить общую цену за товары в заказе
    def total_price(self):
        summ = sum(cart.get_product_price() for cart in self)
        return summ
    #Получить НДС
    def total_NDS(self):
        s = float(sum(cart.get_product_price() for cart in self))
        nds = ((s/1.2) - s)*-1
        return round(nds, 2)
    #Получить скидку на каждый товар в итоге ссумируется в общую
    def get_promo_discaunt(self):
        discaunt = 0
        for i in self:
            try:
                per_sent =float(i.get_product_price()) * float(i.promo_code_id.value_discont/100)
                discaunt +=per_sent
            except AttributeError:
                discaunt = 0
        return round(discaunt, 2)
    #Итоговая сумма общая сумма - общая сумма скидки
    def price_discount(self):
        discount = self.get_promo_discaunt()
        price = self.total_price()
        priceDiscount = float(price) - float(discount)
        return priceDiscount

#Модель заказа
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Пользователь", default=None)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа" )
    order_num = models.CharField(max_length=20, default=RandomOrderNumber(), unique=True, verbose_name='Номер заказа')
    city_delivery = models.CharField(max_length=50, verbose_name="Город доставки")#Данные берем из json файла
    fullNameUser = models.CharField(max_length=200,null=True, blank=True ,verbose_name='ФИО получателя')
    phone = models.CharField(max_length=20, null=True, blank=True ,verbose_name="Номер телефона")
    streetName = models.CharField(max_length=100, null=True, blank=True ,verbose_name="Улица")
    streetNumber = models.CharField(max_length=5, null=True, blank=True, verbose_name="Дом/Номер дома")
    indexNumber = models.CharField(max_length=6, null=True, blank=True, verbose_name="Индекс")
    numberApartment = models.CharField(max_length=5, null=True, blank=True, verbose_name="Квартира")
    statusPay = models.BooleanField(verbose_name='Статус оплаты заказа', default=False)
    adresPostmat = models.CharField(max_length=50, null=True, blank=True, verbose_name='Постамат')
    #В шаблоне не корректная форма для того чтобы правильно связать данные, нет API-карт, улиц, городов,постаматов и так далее (есть просто
    # json с городами))
    #Далее  ForeignKey
    buyerStatus = models.ForeignKey(BuyerStatus, on_delete=models.CASCADE, related_name='BuyerStatus', verbose_name='Заказ от имени')
    methodDelivery = models.ForeignKey(MethodOfObtaining, on_delete=models.CASCADE, related_name='delivery', verbose_name='Способ получения')
    methodPay = models.ForeignKey(PayMethod, on_delete=models.CASCADE, related_name='pay', verbose_name='Способ оплаты')
    total_price = models.CharField(max_length=20, verbose_name='Сумма')#Будем получать из cart.total_price
    totel_nds = models.CharField(max_length=20, verbose_name='НДС')#Будем получать из cart.total_NDS
    promo_discaunt = models.CharField(max_length=20, verbose_name='Скидка')#Будем получать из cart.get_promo_discaunt
    price = models.CharField(max_length=20, verbose_name='Итоговая сумма')#Будем получать из cart.price_discount

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ № {self.pk}| {self.order_num} - Покупатель {self.user.first_name} {self.user.last_name}"

#Промо-код из корзины в заказ для архива
class PromoCode(models.Model):
    code_value = models.CharField(max_length=13, unique=True, null=False, blank=False, verbose_name='Промо-код')
    value_discont = models.SmallIntegerField(verbose_name='% скидки по промо-коду')
    create_code = models.DateTimeField(verbose_name='Дата создания промокода')
    order = models.OneToOneField(Order, on_delete=models.CASCADE,verbose_name='Заказ')
    class Meta:
        verbose_name = 'Промо-код на скидку в заказе'
        verbose_name_plural = 'Промо-коды на скидку в заказах'
    def __str__(self):
        return f'Промокод - {self.code_value} на - {self.value_discont} %'

#Товары в заказе - доделать
class ProductOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order', verbose_name='Заказ')
    #Добавлять из корзины покупок
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='product',verbose_name='Товар')
    name = models.CharField(max_length=100, verbose_name="Название")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")

    class Meta:
        db_table = "order_item"
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"

    orders = OrderItemQueryset.as_manager()

    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self):
        return f"Товар {self.name} | Заказ № {self.order.order_num}"