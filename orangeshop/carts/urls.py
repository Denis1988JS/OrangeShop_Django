from django.urls import path, include, re_path
from carts import views
from carts.views import UserCartView, AddProductCart, RemoveProductCart, ChangeQuantityCart, PromoAddToCart

urlpatterns = [
    path('',UserCartView.as_view(), name='user_cart'),#Страница корзина покупок
    path('add_cart/<int:id>', AddProductCart.as_view(), name='add_card'),#Добавить товар в корзину (+1 шт)
    path('remove_cart/<int:id>', RemoveProductCart.as_view(), name='remove_cart'),#Удалить товар из корзины
    path('changeQuantity/<int:id>',ChangeQuantityCart.as_view(), name='change_quantity'),#Изменить кол-во товара +-
    path('addPromoCode', PromoAddToCart.as_view(), name='addPromoCode'), #Добавить промокод
]

