from django import forms

from orders.models import BuyerStatus, Order, MethodOfObtaining, PayMethod
from .models import *

#Форма модели Order - заказ товара

class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['buyerStatus'].empty_label = None

    class Meta:
        model = Order
        fields = ('buyerStatus','city_delivery','numberApartment','indexNumber', 'methodDelivery','fullNameUser','phone','streetName',
                  'streetNumber',"methodPay")
        widgets = {
            'buyerStatus': forms.RadioSelect(choices=BuyerStatus.objects.all()),
            'city_delivery':forms.TextInput(attrs={'placeholder':'Укажите город', 'type': 'text','class':'form_imput_order'}),
            'methodDelivery': forms.RadioSelect(choices=MethodOfObtaining.objects.all()),
            'methodPay': forms.RadioSelect(choices=PayMethod.objects.all())
        }
