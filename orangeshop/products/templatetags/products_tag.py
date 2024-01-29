from django import template

from products.models import Category

register = template.Library()

@register.inclusion_tag('products/tags/catalog_of_goods_block_relative.html')
def category_list_relative():
    cats_list = Category.objects.all()
    return {'cats_list': cats_list}