from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.
from .models import *


#Модели для товаров-----------------
#Модель цвет продукта - ColorProduct
class ColorProductAdmin(admin.ModelAdmin):
    list_display = ('id','value','get_html_photo')
    list_display_links = ('value',)
    ordering = ['id']
    def get_html_photo(self, object):
        if object.img_color:
            return mark_safe(f"<img src='{object.img_color.url}' width=24 height=24>")
    get_html_photo.short_description = 'Фото'
admin.site.register(ColorProduct,ColorProductAdmin)

#Модель коллекция продукта - Collection + инлайн продукты
class ProductInline(admin.TabularInline):
    model = Product
    classes = ('collapse',)
    extra = 1


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'get_html_photo')
    list_display_links = ('id', 'name',)
    list_editable = ('year',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ("get_html_photo",)
    inlines = [ProductInline]
    fields = [
        ("name",'slug') ,"year",('image','get_html_photo'),'description'
    ]
    ordering = ['id']
    def get_html_photo(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=150 height='auto'>")
    get_html_photo.short_description = 'Фото'
admin.site.register(Collection,CollectionAdmin)

#Модель комплектация товара что в комплекте  - EquipmentProduct
class EquipmentProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name',)
    fields = [
        'name',
        'description'
    ]
admin.site.register(EquipmentProduct, EquipmentProductAdmin)

#Модель статус комплекта  - EquipmentProductSeparately
class EquipmentProductSeparatelyAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')
    list_display_links = ('id', 'value',)
    fields = [
        'value',
    ]
admin.site.register(EquipmentProductSeparately, EquipmentProductSeparatelyAdmin)

#Модель статус комплекта  - EquipmentProductInstance
class EquipmentProductInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_data')
    list_display_links = ('id',)
    fields = ['name','value',]
    def get_data(self, object):
        css_class = 'field-get_data'
        if object.name and object.value:
            return mark_safe(f"<td class={css_class}>{object.name}  {object.value}</td>")
    get_data.short_description = 'Комплектация'
admin.site.register(EquipmentProductInstance , EquipmentProductInstanceAdmin)

#Модель преимущества товара  - Advantages
class AdvantagesProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id','name')
    fields = ['name','description',]
    ordering = ['id']
admin.site.register(AdvantagesProduct, AdvantagesProductAdmin)


#Модель характеристики товара  - Characteristics
class CharacteristicsProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','get_html_photo')
    list_display_links = ('id','title')
    readonly_fields = ("get_html_photo",)
    fields = ['title','description',
              ('image','get_html_photo')]
    ordering = ['id']
    def get_html_photo(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=75 height='auto'>")
    get_html_photo.short_description = 'Фото'

admin.site.register(Characteristics, CharacteristicsProductAdmin)

#Модель категория товаров - Category
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
class CategoryAdmin(MPTTModelAdmin):
    mptt_level_indent = 100
    mptt_indent_field = 'name'
    list_display = ('name', 'parent','get_html_photo','get_html_photo2')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('id', 'get_html_photo','get_html_photo2')
    inlines = [ProductInline]
    fields = [
        ('id', 'name','slug'),
        'parent',
        'description',
        ('image','get_html_photo'),
        ('image2', 'get_html_photo2')
    ]
    def get_html_photo(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=75 height=75 style= object-fit:contain>")
    get_html_photo.short_description = 'Фото'
    def get_html_photo2(self, object):
        if object.image2:
            return mark_safe(f"<img src='{object.image2.url}' width=75 height=75 style= object-fit:contain>")
    get_html_photo2.short_description = 'Фото2'

admin.site.register(Category,CategoryAdmin)

#Модель преимущество категории товаров
class AdvantagesCategoryAdmin(admin.ModelAdmin):
    list_display = ('id',  'categoty')
    list_display_links = ('id', 'categoty')

admin.site.register(AdvantagesCategory,AdvantagesCategoryAdmin)


#Модель товары - Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','price','discount','getSell_price','promo','get_html_photo','category',)
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ("price",'discount','promo')
    list_filter = ('promo', 'category','color','collection','category')
    search_fields = ('name', 'category')
    search_help_text = ('Поиск')
    ordering = ['id']
    
    def get_html_photo(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=35>")
    get_html_photo.short_description = 'Фото'

    def getSell_price(self, obj):
            if obj.discount:
                sell_prise = round(obj.price - obj.price*obj.discount/100, 2)
                return sell_prise
            return obj.price
    getSell_price.short_description = 'Цена со скидкой'
admin.site.register(Product,ProductAdmin)







admin.site.site_title = 'Панель администратора сайта'
admin.site.site_header = 'Панель администратора сайта'
