from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
# Register your models here.

#Админка статус пользователя - BuyerStatus
class BuyerStatusAdmin(admin.ModelAdmin):
    list_display = ('id','status','full_status')
    list_display_links = ('id','status')
admin.site.register(BuyerStatus,BuyerStatusAdmin)

#Админка - способ получения товара MethodOfObtaining
class MethodOfObtainingAdmin(admin.ModelAdmin):
    list_display = ('id','method_name')
    list_display_links = ('id', 'method_name')
admin.site.register(MethodOfObtaining,MethodOfObtainingAdmin)

#Админка - способ оплаты - PayMethod
class PayMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'method_name')
    list_display_links = ('id', 'method_name')
admin.site.register(PayMethod, PayMethodAdmin)

#Инлайн товары в заказе - добавить к Order
class ProductOrderAdminInline(admin.TabularInline):
    model = ProductOrder
    readonly_fields = ("name","product","price","quantity",'getImg')
    can_delete = False
    classes = ('collapse',)
    extra = 0
    def getImg(self, object):
            return mark_safe(f"<img src='{object.product.image.url}' width=50>")
    getImg.short_description = 'Фото'
#Админка - заказ   покупателя - Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','slug','order_num','fullNameUser','user','create_time','statusPay')
    list_display_links = ('id','order_num','fullNameUser','user')
    search_fields = ("order_num",'fullNameUser')
    search_help_text = 'Поиск по заказам - номер или ФИО получателя'
    list_filter = ('methodPay', 'methodDelivery','buyerStatus','statusPay','create_time')
    list_editable = ('statusPay',)
    ordering = ['pk']
    readonly_fields = (
        'user','create_time',"slug","order_num",'methodPay',"statusPay","fullNameUser","phone","buyerStatus",
        "methodDelivery", "adresPostmat", "city_delivery", "streetName", "streetNumber","indexNumber","numberApartment",
        "total_price", "totel_nds", "promo_discaunt", "price"
    )
    inlines = [ProductOrderAdminInline]
    fieldsets = (
        ("Данные о заказе", {
            "fields": (("order_num","slug","create_time","methodPay","statusPay"),)
        }),
        ("Данные о получателе", {
            "fields": (("fullNameUser","user", "phone","buyerStatus"),)
        }),
        ("Данные о доставке", {
            "fields": ("methodDelivery","adresPostmat", ("city_delivery", "streetName","streetNumber","indexNumber","numberApartment"),)
        }),
        ("Итого",{
            "fields": (("total_price", "totel_nds", "promo_discaunt","price"),)
        })
    )
admin.site.register(Order, OrderAdmin)

#Админка - товары в заказе - ProductOrder
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ('id','order','product','price','quantity')
    list_display_links  = ('id','order','product')
    ordering = ['order']
admin.site.register(ProductOrder, ProductOrderAdmin)




#Админка PromoCodeAdmin - активированные промокоды PromoCode
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code_value', 'create_code', 'order')
    list_display_links = ('id', 'code_value', 'create_code', 'order')
    readonly_fields = ('id', 'code_value', 'value_discont','create_code', 'order')
    search_fields = ('order',)
    search_help_text = 'Активированные скидки по заказам'
    fields = (
        ('id', 'code_value', 'order' ),
        ('value_discont', 'create_code'),
    )
admin.site.register(PromoCode, PromoCodeAdmin)