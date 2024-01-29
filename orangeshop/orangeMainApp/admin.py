from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
# Register your models here.
#Модель наши премущества - OurBenefits
class OurBenefitsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image', 'get_img')
    list_display_links = ('id', 'title')
    readonly_fields = ("get_img",)
    fields = [
        'title',
        'description',
        ('image', 'get_img')
    ]
    def get_img(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=75 height=75>")
    get_img.short_description = 'Фото'
admin.site.register(OurBenefits,OurBenefitsAdmin)

#Модель ссылки на соц сети - SocialMedia
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','url', 'image', 'get_img')
    list_display_links = ('id', 'title')
    readonly_fields = ("get_img",)
    fields = [
        'title',
        'url',
        ('image', 'get_img')
    ]
    def get_img(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=75 height=75>")
    get_img.short_description = 'Фото'
admin.site.register(SocialMedia,SocialMediaAdmin)

#Модель фон для блока PromoSectionBG
class PromoSectionBGaAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image', 'get_img')
    list_display_links = ('id', 'title')
    readonly_fields = ("get_img",)
    fields = [
        'title',
        ('image', 'get_img')
    ]
    def get_img(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=100 height=100 style= object-fit:contain>")
    get_img.short_description = 'Фото'

admin.site.register(PromoSectionBG,PromoSectionBGaAdmin)