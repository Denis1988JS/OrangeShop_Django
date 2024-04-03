from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView,View
from django.shortcuts import render, redirect
from carts.models import UserCart
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


