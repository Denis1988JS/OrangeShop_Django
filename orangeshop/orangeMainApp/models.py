from django.db import models

# Create your models here.
#Модель OurBenefits - наши премущества
class OurBenefits(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False,verbose_name='Заголовок')
    description = models.TextField(max_length=1000, blank=False,null=False, verbose_name='Содержиние')
    image = models.ImageField(upload_to="OurBenefits/", verbose_name='Изображение')

    def __str__(self):
        return f'Преимущество - {self.title}'
    class Meta:
        verbose_name = 'Наше преимущество'
        verbose_name_plural =' Наши преимущества'

#Модель SocialMedia - ссылки на соц сети
class SocialMedia(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False,verbose_name='Заголовок')
    url =  models.URLField(blank=False, null=False, unique=True)
    image = models.ImageField(upload_to="SocialMedia/", verbose_name='Изображение ссылки')

    def __str__(self):
        return f'Ссылка - {self.title}'
    class Meta:
        verbose_name = 'Социальная сеть'
        verbose_name_plural ='Социальные сети'

#Модель Фон для блока promo_section
class PromoSectionBG(models.Model):
    title = models.CharField(max_length=100,blank=False, null=False,verbose_name='Заголовок')
    image = models.ImageField(upload_to="PromoSectionBG/", verbose_name='Изображение ссылки')

    def __str__(self):
        return f'Фон - {self.title}'
    class Meta:
        verbose_name = 'Фон для promo_section'
        verbose_name_plural ='Фон для promo_section'