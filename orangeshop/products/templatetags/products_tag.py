from django import template

from products.models import Category, ColorProduct, Collection

register = template.Library()

@register.inclusion_tag('products/tags/catalog_of_goods_block_relative.html')
def category_list_relative():
    cats_list = Category.objects.all()
    return {'cats_list': cats_list}


@register.inclusion_tag('products/tags/color_list_product.html')
#В проекте не применяется
def color_list_product():
    color_list = ColorProduct.objects.all()
    return {'color_list': color_list}

@register.inclusion_tag('products/tags/collection_list_product.html')
#В проекте не применяется
def collection_list_product():
    collection_list = Collection.objects.all()
    return {'collection_list': collection_list}


#Список категорий для мобильной навигации
@register.inclusion_tag('products/tags/mobile_list_of_category.html')
def collection_list_product_mobile():
    category_list = Category.objects.all()
    return {'category_list': category_list}