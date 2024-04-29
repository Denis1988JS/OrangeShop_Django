from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView,View
from django.shortcuts import render, redirect

from carts.forms import OrderForm
from carts.models import UserCart, PromoCode as PromoCodeCart
from carts.templates.utils import CartSumMixin
from orders.models import Order, MethodOfObtaining, PayMethod, BuyerStatus, ProductOrder, PromoCode as PromoCodeOrder


# Create your views here.


class MakeOrder(CartSumMixin,TemplateView):
    template_name = 'orders/take_order.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        context['title'] = "Оформление заказа"
        context['form'] = OrderForm
        carts_list = UserCart.objects.filter(user=self.request.user)
        context = dict(list(context.items()) + list(c_def.items()))
        return context

class AddOrder(CartSumMixin, View):
    def post(self, request):
        # Получаем список товаров в корзине
        carts_list = UserCart.objects.filter(user=self.request.user)
        form = OrderForm(data=request.POST)


        #Проверяем форму на валидность и создаем заказ
        if form.is_valid():
            newOrder = Order()

            #Пользователь и не FK - данные
            newOrder.user = User.objects.get(id=self.request.user.id)
            newOrder.city_delivery = self.request.POST.get('city_delivery')

            if self.request.POST.get('methodDelivery') in ['1','2']:
                newOrder.fullNameUser = self.request.POST.get('fullNameUser')
                newOrder.numberApartment = self.request.POST.get('numberApartment')
                newOrder.indexNumber = self.request.POST.get('indexNumber')
                newOrder.streetName = self.request.POST.get('streetName')
                newOrder.streetNumber = self.request.POST.get('streetNumber')
                newOrder.phone = self.request.POST.get('phone')
            elif  self.request.POST.get('methodDelivery') == '3':
                newOrder.adresPostmat = self.request.POST.get('adresPostmat')

            #FK-данные
            newOrder.buyerStatus = BuyerStatus.objects.get(id=self.request.POST.get('buyerStatus'))
            newOrder.methodDelivery = MethodOfObtaining.objects.get(id=self.request.POST.get('methodDelivery'))
            newOrder.methodPay = PayMethod.objects.get(id=self.request.POST.get('methodPay'))
            if self.request.POST.get('methodPay') in ["2","3"]:
                newOrder.statusPay = True
            else:
                newOrder.statusPay = False
            newOrder.total_price = carts_list.total_price()
            newOrder.totel_nds = carts_list.total_NDS()
            newOrder.promo_discaunt = carts_list.get_promo_discaunt()
            newOrder.price = carts_list.price_discount()
            newOrder.save()
            print('Ok!!!')
            for cart in carts_list:
                product = cart.product
                name = cart.product.name
                quantity = cart.quantity
                price = cart.product.sell_price()
                productOrder = ProductOrder()
                productOrder.order = newOrder
                productOrder.product = product
                productOrder.name = name
                productOrder.price = price
                productOrder.quantity = quantity
                productOrder.save()
            #Получаем промо-код из корзины покупок по id-user
            promoCart = PromoCodeCart.objects.get(user_id=self.request.user.id)
            #Создем промо=код из ордерс
            promoOrder = PromoCodeOrder()
            promoOrder.code_value = promoCart.code_value
            promoOrder.value_discont = promoCart.value_discont
            promoOrder.create_code = promoCart.create_code
            promoOrder.order = newOrder
            promoOrder.save()
            #После внесения всех данных в заказ удаляем корзину пользователя и промо-код
            carts_list.delete()
            promoCart.delete()
            print('Заказ успешно оформлен !!!')
            return redirect("makeOrder")
