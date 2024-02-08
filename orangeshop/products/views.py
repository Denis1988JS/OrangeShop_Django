from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView,View
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from products.models import Product, Category, AdvantagesCategory, Collection
from django.db.models import Q
from django.http import QueryDict

# Create your views here.


#Классовй шаблон - каталог товаров
class CatalogProducts(ListView):
    model = Product
    template_name = 'products/catalog.html'
    context_object_name = 'products'
    paginate_by = 8
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['page_name'] = 'Товары'
        return context

#Классовый шаблон - каталог продукции в разрезе категории
class CatalogProductsCategory(ListView):
    model = Product
    template_name = 'products/catalog_category.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        #Переопределяем модель продукты - к катерии и подкатегиям
        category = Category.objects.get(slug=self.kwargs['category_slug'])
        sub_categories = category.get_descendants(include_self=True)
        queryset = Product.objects.filter(category__in=sub_categories)
        collection_name = self.request.GET.getlist("collection_name")

        return queryset
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Каталог '
        context['category'] = Category.objects.get(slug=self.kwargs['category_slug'])
        context['advantages'] = AdvantagesCategory.objects.filter(categoty__id=context['category'].id)
        context['collection_list'] = Collection.objects.all()
        return context


#Классовый шаблон - каталог продукции в разрезе категории + сортировка + фильрация
class SortCatalogProductsCategory(ListView):
    template_name = 'products/catalog_category.html'
    context_object_name = 'products'
    paginate_by = 2
    def get_queryset(self):
        #Переоределяем  queryset
        print(self.request.GET)
        category = Category.objects.get(slug=self.request.GET.get("category_slug")) #Получаем категорию страницы
        sub_categories = category.get_descendants(include_self=True) #Все субкатегории

        # Обработчики форм и получение из них данных
        if self.request.GET.getlist('collection_name') == []:
            collection_name = list(Collection.objects.all().values_list('name', flat=True))
            print('Список')
        else:
            collection_name = self.request.GET.getlist('collection_name')  # Список коллекций

        print(collection_name)
        print(type(collection_name))
        sub_cat = self.request.GET.getlist("subcategory_slug")[0] # слаг субкатегории
        orderby = self.request.GET.getlist('orderby')[0] #Сортировка из формы



        #Условия если субкатегория либо slug либо all
        if sub_cat == "all":
            #Получаем и возвращаем queryset
            goods = Product.objects.filter(Q(category__in=sub_categories) & Q(collection__name__in = collection_name)).order_by(orderby).distinct()
            if self.request.GET.get('promo') in [None, False, '']:
                goods = Product.objects.filter(Q(category__in=sub_categories)& Q(collection__name__in = collection_name)).order_by(orderby).distinct()
            elif self.request.GET.get('promo') == 'on':
                goods = Product.objects.filter(Q(category__in=sub_categories) & Q(discount__gt=0)& Q(collection__name__in = collection_name)).order_by(orderby).distinct()
        else:
            # Получаем и возвращаем queryset
            goods = Product.objects.filter(Q(category__in=sub_categories) & Q(category__slug=sub_cat)& Q(collection__name__in = collection_name)).order_by(
                orderby).distinct()
            if self.request.GET.get('promo') == 'on':
                goods = Product.objects.filter(Q(category__in=sub_categories) & Q(category__slug=sub_cat)&Q(discount__gt =0)& Q(collection__name__in = collection_name)).order_by(
                    orderby).distinct()


        queryset = goods
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Каталог '
        context['collection_list'] = Collection.objects.all() #Список всех коллекций
        #Данные из GET запросов
        context['category'] = Category.objects.get(slug__in=self.request.GET.getlist("category_slug"))#Категория товаров
        context['orderby'] =  'orderby'+'='+self.request.GET.getlist("orderby")[0]+'&' #Сортировка в пагинацию
        context['subcategory_slug'] = 'subcategory_slug'+'='+self.request.GET.getlist("subcategory_slug")[0]+'&' #Субкатегория в пагинацию
        context['category_slug'] = 'category_slug'+'='+ self.request.GET.getlist("category_slug")[0]+'&'
        context["collection_name"] = ''.join([f"collection_name={x}&" for x in self.request.GET.getlist("collection_name")])
        context['q'] = QueryDict(context["collection_name"]).getlist(key='collection_name') #Список коллекций
        if self.request.GET.get('promo') in [None, False, '']:
            context['promo'] = ''
        else:
            context['promo'] = 'promo'+'='+self.request.GET.getlist('promo')[0]+'&'
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