import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView,View
from django.shortcuts import render, redirect
from carts.models import UserCart, PromoCode
from products.models import Product
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

#Страница - класс корзина товаров пользователя

class UserCartView(LoginRequiredMixin, ListView):
    model = UserCart
    template_name = 'carts/user_cart.html'
    context_object_name = 'carts_list'

    def get_queryset(self):
        #Переопределяем корзину пользователя по id-пользователя из request
        carts_list = UserCart.objects.filter(user = self.request.user)
        return carts_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Корзина - {self.request.user}'
        try:
            context['cupon'] = PromoCode.objects.get(user_id = self.request.user.id)
        except ObjectDoesNotExist:
            context['cupon'] = None
        return context


#Класс - обработчик добавить в корзину товар по id товара
class AddProductCart(TemplateView):

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        product = Product.objects.get(id=kwargs['id'])#Получаем товар

        #Проверяем если пользователь авторизован , то ищем товар в корзине
        if request.user.is_authenticated:
            carts = UserCart.objects.filter(user=user, product = product)
            #Если товар в корзине то ищем первый попавшийся и добавляем +1 к кол-ву
            if carts.exists():
                cart = carts.first()
                if cart:
                    cart.quantity += 1
                    cart.save()
            #Если товара нет в корзине то создаем экземпляр корзины
            else:
                UserCart.objects.create(user = user, product = product, quantity = 1)

        #Если пользователь не авторизован - то корзина по ключу сессии
        else:
            carts = UserCart.objects.filter(session_key=self.request.session_key, product = product)
            if carts.exists():
                cart = carts.first()
                if cart:
                    cart.quantity +=1
                    cart.save()
            #Если товара нет в корзине то создаем экземпляр корзины
            else:
                UserCart.objects.create(session_key=self.request.session_key, product = product, quantity = 1)

        #Возврат на карточку товара + сообщение о то что товар добавлен в корзину
        messages.success(request, f'Товар {product} добавлен в корзину покупок')
        return redirect(product.get_absolute_url())

#Класс удалить товар из корзины пользователя
class RemoveProductCart(TemplateView):
    def get(self, request, *args, **kwargs):
        cart_obj = UserCart.objects.get(id = self.kwargs['id'])
        cart_obj.delete()

        # Возврат в корзину покупок + сообщение о удалении товара
        messages.success(request, f'Товар удален и корзины')
        return redirect('user_cart')

#Изменить кол-во товара +- от 1 до +++++
class ChangeQuantityCart(TemplateView):
    #Запрос без ajax
    def get(self, request, *args, **kwargs):
        val_quantity = int(self.request.GET.get('quantity'))
        cart_obj = UserCart.objects.get(id = self.kwargs['id'])
        print(val_quantity, type(val_quantity), cart_obj.quantity, type(cart_obj.quantity))
        if val_quantity == -1 and cart_obj.quantity > 1:
            print('-')
            cart_obj.quantity = cart_obj.quantity - 1
            cart_obj.save()
        elif val_quantity == 1:
            print('+')
            cart_obj.quantity = cart_obj.quantity + 1
            cart_obj.save()
        return redirect('user_cart')

#Добавить к корзине купон на скидку - промо-код

class PromoAddToCart(TemplateView):
    def get(self, request, *args, **kwargs):
        promo_code = str(self.request.GET.get("promo_code"))
        #Обработчики ошибок
        try:
            promo = PromoCode.objects.get(code_value=promo_code, is_active=True, user_cart_id = None)
            #Промо-код - обновляем user_id в promo присоединяем пользователя к промо-коду + меняем что код не активный и дату когда применили
            promo.user_id = User.objects.get(id = self.request.user.id) #Пользователь
            promo.activate_code = datetime.datetime.now()#Дата применения промо-кода
            promo.is_active = False #Что промо-код не активный
            promo.save()
            #Корзина покупок - получаем корзины покупок и к ним присоединяем - промокоды чтобы получить скидку
            user_cart = UserCart.objects.filter(user = self.request.user)
            for cart in user_cart:
                cart.promo_code_id = promo
                print(cart.product, '1', 'готово')
                cart.save()

            messages.success(request, f'У вас скидка ₽ ({promo.value_discont}%)')
        except ObjectDoesNotExist:
            messages.warning(request, f'Промо-код не действителен')
        except MultipleObjectsReturned:
            messages.warning(request, f'Промо-код не действителен')
        return redirect('user_cart')

