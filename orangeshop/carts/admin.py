from django.contrib import admin
from django.utils.safestring import mark_safe
# Register your models here.

from .models import PromoCode, UserCart


#Админка - промокод
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('id','code_value','value_discont','user_id','user_cart_id','is_active')
    list_display_links = ('id', 'code_value')
    search_fields = ("code_value",)
    list_editable = ('is_active',)
    list_filter = ('value_discont','is_active')
    readonly_fields = ("create_code","activate_code")

    fields = (
            ("code_value","value_discont","is_active"),
            ("user_cart_id","user_id"),
            ("create_code", "activate_code")
    )

admin.site.register(PromoCode,PromoCodeAdmin)

#Inline для корзины покупок
class UserCartAdminInline(admin.TabularInline):
    model = UserCart
    readonly_fields = ("create_time",)
    fields = (('user', 'product', 'quantity'),
              ('session_key','create_time'))
    extra = 1

#Админка - корзина покупок пользователя
class UserCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity','create_time','session_key','promo_code_id')
    list_display_links = ('id', 'user')
    search_fields = ("user",)
    list_filter = ('user', 'product')
    readonly_fields = ("create_time",)
    fields = (('user', 'product', 'quantity','promo_code_id'),
              ('session_key','create_time'))
admin.site.register(UserCart, UserCartAdmin)

