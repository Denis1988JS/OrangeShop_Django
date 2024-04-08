from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from carts.admin import UserCartAdminInline
from  .models import UserBuyersData
# Register your models here.

from django.contrib import admin


#Админка модель данные о покупателе - UserBuyersData
class UserBuyersDataAdmin(admin.ModelAdmin):
    list_display = ('id','user','nick_name','get_image')
    list_display_links = ('id', 'user', 'nick_name')
    ordering = ['pk']
    search_fields = ('user', 'nick_name',)
    search_help_text = 'Поиск по пользователям'

    def get_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=50>")
    get_image.short_description = 'Фото'
admin.site.register(UserBuyersData, UserBuyersDataAdmin)


#Админка основная + инлайн UserBuyersData
class UserBuyersDataInline(admin.TabularInline):
    model = UserBuyersData
    classes = ('collapse',)
    extra = 1
    readonly_fields = ('getImg',)
    def getImg(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=100>")
    getImg.short_description = 'Главное фото'

class UserAdmin(admin.ModelAdmin):
    inlines = [UserBuyersDataInline, UserCartAdminInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)