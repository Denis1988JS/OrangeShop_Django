from django.contrib import admin
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

#Админка - заказ покупателя - Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','order_num','fullNameUser','user','create_time','statusPay')
    list_display_links = ('id','order_num','fullNameUser','user')
    search_fields = ("order_num",'fullNameUser')
    list_filter = ('methodPay', 'methodDelivery','buyerStatus','statusPay')
    ordering = ['pk']
admin.site.register(Order, OrderAdmin)

#Админка - товары в заказе - ProductOrder
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ('id','order','product','price','quantity')
    list_display_links  = ('id','order','product')
    ordering = ['order']
admin.site.register(ProductOrder, ProductOrderAdmin)