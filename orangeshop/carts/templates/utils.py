#Миксин отображает сумму к оплате в корзине
from carts.models import UserCart

class CartSumMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['carts_list'] = UserCart.objects.filter(user=self.request.user)
        return context