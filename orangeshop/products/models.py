from django.db import models
from datetime import date
from django.urls import reverse, reverse_lazy


# Create your models here.

#--------------Модели для товаров
#Модель цвет товара - ColorProduct
class ColorProduct(models.Model):
    value = models.CharField(max_length=20, unique=True, verbose_name='Название цвета', null=False, blank=False)
    img_color = models.ImageField(upload_to="ColorProduct/", verbose_name='Фото',null=False, blank=False )

    def __str__(self):
        return self.value
    class Meta:
        verbose_name = 'Цвет товара'
        verbose_name_plural = 'Цвет товаров'

#Модель коллекция товара - Collection
class Collection(models.Model):
        name = models.CharField(max_length=50, unique=True, null=False, blank=False, verbose_name='Название колекции')
        description = models.TextField(max_length=500, null=False, blank=False, verbose_name='Описание колекции')
        slug = models.SlugField(max_length=50, unique=True, null=False, blank=False, db_index=True, verbose_name='URL-коллекции')
        year = models.CharField(max_length=4, null=False, blank=False, verbose_name='Год выпуска коллекции')
        image = models.ImageField(upload_to="Collection/", verbose_name='Фото коллекции', null=False, blank=False )

        def __str__(self):
            return f'Коллекция - {self.name}'
        def get_absolute_url(self):
            return reverse('collection', kwargs={'collection_slug': self.slug})
        class Meta:
            verbose_name = 'Коллекция товара'
            verbose_name_plural = 'Коллекция товаров'

#Модель комплектация товара - EquipmentProduct
class EquipmentProduct(models.Model):
        name = models.CharField(max_length=150, verbose_name='Комплектация')
        description = models.TextField(max_length=200, verbose_name='Описание комплектации')
        def __str__(self):
            return f'{self.name}'
        class Meta:
            verbose_name = 'Комплектация товара'
            verbose_name_plural = 'Комплектация товаров'

#Модель характеристика комплектации - EquipmentProductSeparately (отдельно или кол-во)
class EquipmentProductSeparately(models.Model):
        value = models.CharField(max_length=50, verbose_name='Характеристика комплектации', help_text='Указать либо приобретать отдельно либо '
                                                                                                      'кол-во')
        def __str__(self):
            return f'Статус комплектации - {self.value}'
        class Meta:
            verbose_name = 'Статус комплектации'
            verbose_name_plural = 'Статус комплектации'

#Модель комплектация товара экземпляр - EquipmentProductInstance - к модели продукта MTM
class EquipmentProductInstance(models.Model):
    name = models.ForeignKey(EquipmentProduct, on_delete=models.CASCADE, verbose_name="Комплектация", related_name='equipment')
    value = models.ForeignKey(EquipmentProductSeparately, on_delete=models.CASCADE, verbose_name="Характеристика", related_name='separately')
    def __str__(self):
        return f'Экземпляр комплектации - {self.name}'
    class Meta:
        verbose_name = 'Экземпляр комплектации товара'
        verbose_name_plural = 'Экземпляры комплектации товаров'


#Модель преимущества товаров Advantages  - к модели продукта MTM
class AdvantagesProduct(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False, verbose_name='Преимущество товара')
    description = models.TextField(max_length=500, unique=True, null=False, blank=False, verbose_name='Описание преимущества товара')
    def __str__(self):
        return f'Преимущество товара - {self.name}'
    class Meta:
        verbose_name = 'Преимущество товара'
        verbose_name_plural = 'Преимущества товаров'


#Модель характеристики товара Characteristics   - к модели продукта MTM
class Characteristics(models.Model):
    title = models.CharField(max_length=50, unique=True, null=False, blank=False, verbose_name='Характеристика')
    description = models.TextField(max_length=500, unique=True, null=False, blank=False, verbose_name='Описание характеристики')
    image = models.ImageField(upload_to="Characteristics/", verbose_name='Характеристика фото')

    def __str__(self):
        return f'Характеристика - {self.title}'
    class Meta:
        verbose_name = 'Характеристика товара'
        verbose_name_plural = 'Характеристики товаров'

#----------Модели категория товаров
from mptt.models import MPTTModel, TreeForeignKey

#Модель категория товаров - Category
class Category(MPTTModel):
    name = models.CharField(max_length=50,  unique=True, null=False, blank=False, verbose_name='Название категории')
    slug = models.SlugField(max_length=50, unique=True, null=False, blank=False, db_index=True, verbose_name='URL-категории')
    image = models.ImageField(upload_to="Categoty/", verbose_name='Фото категории')
    image2 = models.ImageField(upload_to="Categoty_2/" ,null=True, blank=True, verbose_name='Фото 2 категории')
    description = models.TextField(max_length=2000, unique=True, verbose_name='Описание категории')
    parent = TreeForeignKey(
        'self',
        related_name="children",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug':self.slug})

    class MPTTMeta:
        order_insertion_by = ['name']
    class Meta:
        unique_together = [['parent', 'slug']]
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'



#Модель преимущество категории - AdvantagesCategory
class AdvantagesCategory(models.Model):
    description = models.TextField(max_length=500, unique=True, null=False, blank=False, verbose_name='Преимущество')
    categoty = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория", related_name='cat' )
    def __str__(self):
        return f'Категория - {self.description}'
    class Meta:
        verbose_name = 'Преимущество категории'
        verbose_name_plural = 'Преимущества категорий'


#---------Модель товары--------

#Модель товар - Product
class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False, verbose_name='Название товара')
    slug = models.SlugField(max_length=100, unique=True, null=False, blank=False, db_index=True, verbose_name='URL-товара')
    short_description = models.TextField(max_length=500, unique=True, null=False, blank=False, verbose_name='Краткое описание товара')
    description = models.TextField(max_length=1000, unique=True, null=False, blank=False, verbose_name='Полное описание товара')
    promo = models.BooleanField(default=False, verbose_name='Акционный товар')
    image = models.ImageField(upload_to="Product/", verbose_name='Главное фото товара')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в %')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Остаток')
    color = models.ManyToManyField(ColorProduct, related_name='color', verbose_name='Цвет товара')
    collection  = models.ForeignKey(Collection, on_delete=models.CASCADE, verbose_name="Коллекция")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    time_create  = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания товара')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления товара')
    equipment  = models.ManyToManyField(EquipmentProductInstance, related_name='equipment', verbose_name='Комплектация товара')
    advantages  = models.ManyToManyField(AdvantagesProduct,  related_name='advantages', verbose_name='Преимущества товара')
    connectionDiagram = models.ImageField(upload_to='connectionDiagram/', verbose_name='Схема подключения или монтажа')
    characteristics  = models.ManyToManyField(Characteristics, related_name='characteristics', verbose_name='Характеристики товара' )

    def __str__(self):
        return f'Товар - {self.name}'

    def sell_price(self):
        if self.discount:
            return round(self.price - (self.price*self.discount/100), 0)
        return self.price

    def setPromo(self):
        if self.discount > 0:
            self.promo = True
            return self.promo

    def get_absolute_url(self):
        return reverse_lazy('product', kwargs={'product_slug':self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'





