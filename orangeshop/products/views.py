from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView,View
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from carts.templates.utils import CartSumMixin
from orangeMainApp.models import OurBenefits
from products.models import Product, Category, AdvantagesCategory, Collection, ColorProduct
from django.db.models import Q
from django.http import QueryDict

# Create your views here.


#Классовый шаблон - каталог товаров
class CatalogProducts(CartSumMixin,ListView):
    model = Product
    template_name = 'products/catalog.html'
    context_object_name = 'products'
    paginate_by = 8
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        context['title'] = 'Каталог'
        context['page_name'] = 'Товары'
        context = dict(list(context.items()) + list(c_def.items()))
        return context

#Классовый шаблон - каталог продукции в разрезе категории
class CatalogProductsCategory(CartSumMixin,ListView):
    model = Product
    template_name = 'products/catalog_category.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        #Переопределяем модель продукты - к катерии и подкатегиям
        category = Category.objects.get(slug=self.kwargs['category_slug'])
        sub_categories = category.get_descendants(include_self=True)
        queryset = Product.objects.filter(category__in=sub_categories)
        collection_name = self.request.GET.getlist("collection_name")
        return queryset
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        context['title'] = f'Каталог '
        context['category'] = Category.objects.get(slug=self.kwargs['category_slug'])
        context['advantages'] = AdvantagesCategory.objects.filter(categoty__id=context['category'].id)
        context['collection_list'] = Collection.objects.all()
        context['color_list'] = ColorProduct.objects.all()  # Список всех цветов коллекци
        context = dict(list(context.items()) + list(c_def.items()))
        return context


#Классовый шаблон - каталог продукции в разрезе категории + сортировка + фильрация
class SortCatalogProductsCategory(CartSumMixin, ListView):
    template_name = 'products/catalog_category.html'
    context_object_name = 'products'
    paginate_by = 6
    def get_queryset(self):
        #Переоределяем  queryset
        category = Category.objects.get(slug=self.request.GET.get("category_slug")) #Получаем категорию страницы
        sub_categories = category.get_descendants(include_self=True) #Все субкатегории
        # Обработчики форм и получение из них данных
        #Получаем данные из коллекции товара
        if self.request.GET.getlist('collection_name') == []:
            collection_name = list(Collection.objects.all().values_list('name', flat=True))
        else:
            collection_name = self.request.GET.getlist('collection_name')  # Список коллекций

        #Получаем данные из цвета товара
        if self.request.GET.getlist('color_name') == []:
            color_list = list(ColorProduct.objects.all().values_list('value', flat=True))

        else:
            color_list = self.request.GET.getlist('color_name')  # Список цветов


        sub_cat = self.request.GET.getlist("subcategory_slug")[0] # слаг субкатегории
        orderby = self.request.GET.getlist('orderby')[0] #Сортировка из формы

        #Условия если субкатегория либо slug либо all
        if sub_cat == "all":
            #Получаем и возвращаем queryset
            goods = Product.objects.filter(Q(category__in=sub_categories) & Q(collection__name__in = collection_name) & Q(color__value__in =
                                                                                                                         color_list)).order_by(orderby).distinct()
            if self.request.GET.get('promo') in [None, False, '']:
                goods = Product.objects.filter(Q(category__in=sub_categories)& Q(collection__name__in = collection_name) & Q(color__value__in =
                                                                                                                         color_list)).order_by(
                    orderby).distinct()
            elif self.request.GET.get('promo') == 'on':
                goods = Product.objects.filter(Q(category__in=sub_categories) & Q(discount__gt=0) & Q(collection__name__in =
                                                                                                      collection_name) & Q(color__value__in =
                                                                                                                         color_list)).order_by(
                    orderby).distinct()
        else:
            # Получаем и возвращаем queryset
            goods = Product.objects.filter(Q(category__in=sub_categories) & Q(category__slug=sub_cat) & Q(collection__name__in =
                                                                                                          collection_name) & Q(color__value__in =
                                                                                                                         color_list)).order_by(
                orderby).distinct()
            if self.request.GET.get('promo') == 'on':
                goods = Product.objects.filter(Q(category__in=sub_categories) & Q(category__slug=sub_cat)&Q(discount__gt =0)& Q(
                    collection__name__in = collection_name) & Q(color__value__in =
                                                                                                                         color_list)).order_by(
                    orderby).distinct()

        queryset = goods
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        context['title'] = f'Каталог '
        context['collection_list'] = Collection.objects.all() #Список всех коллекций
        context['color_list'] = ColorProduct.objects.all()#Список всех цветов коллекций
        #Данные из GET запросов
        context['category'] = Category.objects.get(slug__in=self.request.GET.getlist("category_slug"))#Категория товаров
        context['orderby'] =  'orderby'+'='+self.request.GET.getlist("orderby")[0]+'&' #Сортировка в пагинацию
        context['subcategory_slug'] = 'subcategory_slug'+'='+self.request.GET.getlist("subcategory_slug")[0]+'&' #Субкатегория в пагинацию
        context['category_slug'] = 'category_slug'+'='+ self.request.GET.getlist("category_slug")[0]+'&'
        context["collection_name"] = ''.join([f"collection_name={x}&" for x in self.request.GET.getlist("collection_name")])
        context["color_list_get"] = ''.join([f"color_name={x}&" for x in self.request.GET.getlist("color_name")])#Цвета в пагинацию
        context['q'] = QueryDict(context["collection_name"]).getlist(key='collection_name') #Список коллекций
        context['c'] = QueryDict(context["color_list_get"]).getlist(key='color_name')  # Список цветов
        if self.request.GET.get('promo') in [None, False, '']:
            context['promo'] = ''
        else:
            context['promo'] = 'promo'+'='+self.request.GET.getlist('promo')[0]+'&'
        context = dict(list(context.items()) + list(c_def.items()))
        return context

# sub_category = self.request.GET.getlist("subcategory_slug")[0]
# collection_name = self.request.GET.getlist("collection_name")
# category = Category.objects.get(slug__in=self.request.GET.getlist("category_slug"))
# sub_categories = category.get_descendants(include_self=True)
# sort = self.request.GET.getlist("orderby")[0]
# promo_true = self.request.GET.getlist("promo_goods")[0]
# print(promo_true)
 # if sub_category == 'all'  or sub_category == '+all':
#     queryset = Product.objects.filter(Q(category__in=sub_categories) & Q(promo=promo_true)).order_by(sort).distinct()
#     if len(collection_name) > 0:
#         queryset = Product.objects.filter(Q(category__in=sub_categories) & Q(collection__name__in = collection_name)& Q(promo=promo_true)).distinct().order_by(sort)
#     return queryset
#
# elif sub_category != 'all':
#     queryset = Product.objects.filter(category__slug=sub_category).order_by(sort).distinct()
#     if len(collection_name) > 0:
#         queryset = Product.objects.filter(Q(category__slug=sub_category) & Q(collection__name__in = collection_name)& Q(promo=promo_true)).distinct().order_by(sort)

# context['category_slug'] = 'category_slug'+'='+self.request.GET.getlist("category_slug")[0]+'&'
# context['orderby'] = 'orderby'+'='+self.request.GET.getlist("orderby")[0]+'&'
# context['subcategory_slug'] = 'subcategory_slug'+'='+self.request.GET.getlist("subcategory_slug")[0] +'&'
# context['category'] = Category.objects.get(slug__in=self.request.GET.getlist("category_slug"))
# context['advantages'] = AdvantagesCategory.objects.filter(categoty__id=context['category'].id)
# context['collection_list'] = Collection.objects.all()
# context["collection_name"] = ''.join([f"collection_name={x}&" for x in self.request.GET.getlist("collection_name")])
# context["promo"] = 'promo'+'='+self.request.GET.getlist("promo_goods")[0] +'&'
# context['q'] = QueryDict(context["collection_name"]).getlist(key='collection_name')

#Класс - о товаре отдельно
class ProductView(CartSumMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        context['benefits'] = OurBenefits.objects.all()
        context['other_product'] = Product.objects.filter(collection_id=self.object.collection.id)[0:4]
        context = dict(list(context.items()) + list(c_def.items()))
        return context

#Класс - поиск на сайте
class SeachProduct(CartSumMixin,ListView):
    template_name = 'products/seach_result.html'
    paginate_by = 6
    context_object_name = 'products'
    #Переопределяем запрос - поиск по какому либо символу(символам) среди товаров
    def get_queryset(self):
        #Список коллекций
        if self.request.GET.getlist('collection_name'):
            collection_name = self.request.GET.getlist('collection_name')
        else:
            collection_name = list(Collection.objects.all().values_list('name', flat=True))
        #Акционный товар или нет
        if self.request.GET.get('promo') == 'on':
            promo = 'on'
        else:
            promo = False
        # Сортировка - если есть в request то значение из request если нет то name
        if self.request.GET.get("orderby") != 'name':
            orderby = self.request.GET.get("orderby")
        elif self.request.GET.get("orderby") == None or self.request.GET.get("orderby") =="":
            orderby = 'name'
        else:
            orderby = 'name'
        # Список цветов если есть в request то значение из request если нет то все цвета (список)
        if self.request.GET.getlist('color_name'):
            color_list = self.request.GET.getlist('color_name')
        else:
            color_list = list(ColorProduct.objects.all().values_list('value', flat=True))

        if orderby or color_list or collection_name:
            goods = Product.objects.filter(
                Q(name__icontains=self.request.GET.get("seach"))&
                Q(color__value__in = color_list) & Q(
                    collection__name__in = collection_name)).order_by(orderby).distinct()
            
        if promo == 'on':
            goods = Product.objects.filter(
                Q(name__icontains=self.request.GET.get("seach")) &
                Q(color__value__in=color_list)&
                Q(discount__gt = 0) &
                Q(collection__name__in = collection_name)).order_by(orderby).distinct()
        else:
            goods =  Product.objects.filter(name__icontains=self.request.GET.get("seach")).order_by(orderby).distinct()
        queryset = goods
        return queryset
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        c_def = self.get_user_context()
        context['title'] = f'Поиск по {self.request.GET.get("seach")} ' #title
        context['data'] = self.request.GET.get("seach") #Запрос get
        context['seach'] = f'seach={self.request.GET.get("seach")}&' #Для пагинации что искали
        context['orderby'] = f'orderby={self.request.GET.get("orderby")}&'  # Сортировка в пагинацию
        context["color_list_get"] = ''.join([f"color_name={x}&" for x in self.request.GET.getlist("color_name")])
        context['color_list'] = ColorProduct.objects.all()  # Список всех цветов коллекций
        context['collection_list'] = Collection.objects.all()  # Список всех коллекций
        context["collection_name"] = ''.join([f"collection_name={x}&" for x in self.request.GET.getlist("collection_name")])#Коллекци в пагинацию
        context['c'] = QueryDict(context["color_list_get"]).getlist(key='color_name')#Цвета в GET
        context['q'] = QueryDict(context["collection_name"]).getlist(key='collection_name')  # Список коллекций
        if self.request.GET.get('promo') in [None, False, '']:
            context['promo'] = ''
        else:
            context['promo'] = 'promo'+'='+self.request.GET.getlist('promo')[0]+'&'
        context = dict(list(context.items()) + list(c_def.items()))
        return context