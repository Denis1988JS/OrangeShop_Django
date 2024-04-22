# Generated by Django 5.0.1 on 2024-04-16 15:27

import django.db.models.deletion
import django.db.models.manager
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0005_alter_category_unique_together_advantagescategory'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyerStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20, verbose_name='Статус (заказ от имени)')),
                ('full_status', models.CharField(max_length=50, verbose_name='Полное наименование')),
            ],
            options={
                'verbose_name': 'Статус покупателя',
                'verbose_name_plural': 'Статусы покупателей',
            },
        ),
        migrations.CreateModel(
            name='MethodOfObtaining',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method_name', models.CharField(max_length=20, verbose_name='Способ получения')),
            ],
            options={
                'verbose_name': 'Способ получения заказа',
                'verbose_name_plural': 'Способы получения заказов',
            },
        ),
        migrations.CreateModel(
            name='PayMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method_name', models.CharField(max_length=20, verbose_name='Метод оплаты')),
            ],
            options={
                'verbose_name': 'Метод оплаты заказа',
                'verbose_name_plural': 'Методы оплаты заказов',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')),
                ('order_num', models.CharField(default='R202441622273150', max_length=20, unique=True, verbose_name='Номер заказа')),
                ('city_delivery', models.CharField(max_length=50, verbose_name='Город доставки')),
                ('fullNameUser', models.CharField(blank=True, max_length=200, null=True, verbose_name='ФИО получателя')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер телефона')),
                ('streetName', models.CharField(blank=True, max_length=100, null=True, verbose_name='Улица')),
                ('streetNumber', models.CharField(blank=True, max_length=5, null=True, verbose_name='Дом/Номер дома')),
                ('indexNumber', models.CharField(blank=True, max_length=6, null=True, verbose_name='Индекс')),
                ('numberApartment', models.CharField(blank=True, max_length=5, null=True, verbose_name='Квартира')),
                ('statusPay', models.BooleanField(default=False, verbose_name='Статус оплаты заказа')),
                ('adresPostmat', models.CharField(blank=True, max_length=50, null=True, verbose_name='Постамат')),
                ('total_price', models.CharField(max_length=20, verbose_name='Сумма')),
                ('totel_nds', models.CharField(max_length=20, verbose_name='НДС')),
                ('promo_discaunt', models.CharField(max_length=20, verbose_name='Скидка')),
                ('price', models.CharField(max_length=20, verbose_name='Итоговая сумма')),
                ('buyerStatus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BuyerStatus', to='orders.buyerstatus', verbose_name='Заказ от имени')),
                ('methodDelivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery', to='orders.methodofobtaining', verbose_name='Способ получения')),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('methodPay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pay', to='orders.paymethod', verbose_name='Способ оплаты')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='orders.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='products.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Проданный товар',
                'verbose_name_plural': 'Проданные товары',
                'db_table': 'order_item',
            },
            managers=[
                ('orders', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_value', models.CharField(max_length=13, unique=True, verbose_name='Промо-код')),
                ('value_discont', models.SmallIntegerField(verbose_name='% скидки по промо-коду')),
                ('create_code', models.DateTimeField(verbose_name='Дата создания промокода')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Промо-код на скидку в заказе',
                'verbose_name_plural': 'Промо-коды на скидку в заказах',
            },
        ),
    ]
