from django import template
from products.models import Category, Collection, Product
from orangeMainApp.models import OurBenefits , PromoSectionBG
from django.db.models import Min
register = template.Library()

@register.inclusion_tag('orangeMainApp/tags/our_products_cart_list.html')
def our_products_cart_list():
    cats_list = Category.objects.all()
    return {'cats_list': cats_list}


@register.inclusion_tag('orangeMainApp/tags/collection_info_section.html')
def collection_first():
    collection = Collection.objects.first()
    all_product  = collection.product_set.all()
    min_price = all_product.aggregate(Min("price"))
    return {'collection': collection, 'min_price':min_price['price__min']}


@register.inclusion_tag('orangeMainApp/tags/promo_product_list.html')
def product_promo_list():
    product_promo = Product.objects.filter(promo=True)[:4]
    return {'product_promo': product_promo}


@register.inclusion_tag('orangeMainApp/tags/our_benefits_list.html')
def our_benefits_list():
    our_benefits = OurBenefits.objects.all()
    return {'our_benefits': our_benefits}

@register.inclusion_tag('orangeMainApp/tags/promo_section.html')
def our_promo_list():
    sliders = PromoSectionBG.objects.all()
    return {'sliders': sliders}

