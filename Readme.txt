Web - приложение - интернет магазин по продаже сантехники - ORANGE

Главные цели проекта выполнены... 

НЕЕЕЕЕ Кроссбраузерная только Crome, адаптив 576-1200px - придумал сам так как в макете его нет

НЕЕЕЕ пиксель в пиксель - много что в проект добавил сам 

Цель проекта - реализовать основные функции Django а именно - Работа с базой данных, модели, формы моделей, взаимодействие спользователем (регистрация, авторизация, выход с сайта), админ панель сайта..
Реализация модели товаров в разрезе товарных категорий и подкатегорий, фозможность фильтрации и сортировки товаров на сайте, вывода как товаров по категории так и детально
Возможность ЗАРЕГИСТРИРОВАННОГО пользователя - добавлять товары в корзину (далее удалить, увеличить или уменьшить кол-во товаров), применить промо-код
Возможность на основе корзины сделать - ЗАКАЗ
В заказе - реализованы введение адреса, типа поставки (нет карты по причине отсутсвия бесплатно API maps), функционал оплаты - либо карта либо Тинькоф (без валидаций а простое внесение данных - имитация карты)



----------------Структура web-приложения ----------------
1.Приложение main - главное приложение, где отображена главная страница сайта + прочие страницы 
	Страницы приложения main:
		- home- главная страница ГОТОВО !
		- about_company - о компании
		- cooperation - сотрудничество
		- where_to_buy - где купить
		- service_maintenance - сервисное обслуживание
		- contacts - контакты
		- buyers - покупателям
		- about_products - о продукции

	Модели приложения main:
		our-benefits - наши преимущества ГОТОВО !
		social-media - ссылки на социальные сети ГОТОВО !
	
2.Приложение products - товары

	Страницы приложения products:
		- products_catalog - наша продукция (вся продукция 8 шт + пагинация) ГОТОВО !
		- product - продукт (один продукт по слагу) ГОТОВО !
		- promotional_goods - акционные товары (вся продукция с акциями 9 шт + пагинация + фильтры)
		- category - категория (категория слаг + продукты категории) ГОТОВО !
		- collection - коллекция (коллекция слаг + продукты коллекции)		
		- search - результат поиска на сайте ГОТОВО !


3.Приложение users - пользователи 

	Страницы приложения users:
		- registration - регистрация пользователя ГОТОВО !
		- login - авторизация пользователя ГОТОВО !
		- profile - личный кабинет пользователя ГОТОВО!
		- logout - выход с сайта


4.Приложение carts - корзина покупок
	Страницы приложения carts:
		- cart - корзина покупок пользователя
		- cart_add - добавить товар в коризну
		- cart_change - поменять кол-во товара
		- cart_delete - удалить товар из корзины


5.Приложение orders - заказ покупателя: ГОТОВО
	Страницы приложения orders:
		- create-order - форма заказа покупателя




---------------------Структура страниц (содержимое)-----------------

1. Главная страница - home - отдельное приложение для отображения информации - orangeMainApp - ГОТОВО !
	- Header сайта (Навигация + слайдер + меню) +
	- Описание Orange - templatetag +
	- Блок ссылки - продукция по категориям +
   	- Блок ссылка - продукция какой либо коллекции +
	- Блок ссылки - акционные товары + сделать слайдером 4-2-1 карточка товара + (слайдера нет)
	- Наши преимущества - templatetag +
	- Блок пункт характеристики компании + фото +
	- Footer сайта +

2.Страница по категориям - category/slug : ГОТОВО !
	- Header сайта (Навигация + слайдер + меню)+
	- Главный блок :+
		- Фильтрация по назначению товара+
		- Сортировка+
		- Фильтрация по характеристикам товара+
		- Блок вывода товаров по категории + пагинация+
	- Блок описание категории товара+
	- Footer сайта+

3.Страница каталог товаров - ''(products main): ГОТОВО !
	- Header сайта (Навигация + слайдер + меню)+
	- Блок ссылки - продукция по категориям+
	- Блок наши товары + пагинация+
	- Блок описание продукции+
	- Footer сайта+

4.Страница карточка товара - product по слагу: ГОТОВО !
	- Header сайта (Навигация + слайдер + меню) +
	- Блок карточка товара+
	- Блок характеристики товара (или что в комплекте)+
	- Блок пункт характеристики компании + фото +
	- Блок 4 случайных товара из коллекции товара по слагу+
	- Блок 1 преимущество + ссылка +
	- Footer сайта+

5.Страница корзина покупок cart по пользователю: ГОТОВО
	- Header сайта (Навигация + слайдер + меню)
	- Блок моя корзина + активация промокода
	- Footer сайта
	

6.Страница заказ/оформление заказа:ГОТОВО
	- Header сайта (Навигация + слайдер + меню)
	- Форма оформления заказа
	- Состав заказа 
	- Footer сайта

7.Личный кабинет пользователя/профиль: ГОТОВО !
	- Header сайта (Навигация + слайдер + меню)+
	- Карточка профиль пользователя + Редактировать профиль+
	- Footer сайта+

8.Заказы пользователя:ГОТОВО
	- Header сайта (Навигация + слайдер + меню)
	- Карточка профиль пользователя + Список заказов
	- Footer сайта




-----Модели и приложения--------Предварительные!!! - по ходу создания проекта могут быть изменения

-------Модель товары и с ним связанные приложение products -----------
1. Product - модель товар ГОТОВО !
	-id
	-name - название
	-slug - слаг
	-appointment - назначение краткое описание товара
	-description - описание
	-promo - акционный товар
	-image - фото
	-price - цена
	-discount - скидка
	-color - внешний на модель цвет MTM(можно выбрать несколько цветов) + ColorProduct
	-collection - внешний на модель коллекция FK +
	-category - внешний на модель категория FK +
	-created  - дата создания товара
	-updated - дата изменения товара
	-stock - остаток товара на складе
	-equipment - комплектация MTM
	-advantages - преимущества товара MTM
	-connectionDiagram - схема подключения (фото, необязательно)
	-characteristics - характеристики товара  MTM

1.1 ColorProduct- модель цвет товара - ГОТОВО (цвет товара + фото цвета + ОК) - в админке ГОТОВО !
	-id
	-value
	-img
 
1.2 Collection - модель коллекция товаров ГОТОВО(ОК) - в админке ГОТОВО !
	-id
	-name - название коллекции
	-slug - слаг коллекции
	-year - год коллекции
	-image - фото коллекции
	-description - описание коллекции

---------------------

	БЛОК на странице что в комплекте

1.3 EquipmentProduct- модель комплектация товара что в комплекте ГОТОВО (ОК)
	-id
	-name
	-description 

1.3.1 EquipmentProductSeparately- статус комплекта (отдельно ил кол-во) ГОТОВО (ОК)
	-id
	-value

1.3.1 EquipmentProductInstance- модель комплектация товара - экземпляр то что привязываем к товару ГОТОВО ManyToManyField - в Админке
	-id
	-name FK - EquipmentProduct
	-value - FK - EquipmentProductSeparately
---------------
	БЛОК - преимущества
1.4 Advantages - модель преимущества товара ГОТОВО (ок) ManyToManyField - Готово в админке
	-id
	-name
	-description 
---------------
	БЛОК -характеристики
1.5 Characteristics - модель характеристики товара ГОТОВО (ок) ManyToManyField - Готово в админке
	-id
	-name
	-value
	-img

-------------------------------------------------------

-------Модель категория и с ним связанные ------------
2. Category - модель категория товара - реализация через  пакет django-mptt и django-mptt-admin ГОТОВО - Готово в админке
	-id
	-name - название
	-slug - слаг
	-image - фото
	-description - описание категории товара
	-parent - self субкатегория

2.1 Advantages - модель преимущества категории ГОТОВО - Готово в админке
	-id
	-description - описание преимущества
	-сategory - fk - на модель категории

--------Модели приложения main
OurBenefits: - модель наши преимущества ГОТОВО - Готово в админке
	-id
	title
	description
	image

SocialMedia: - модель ссылки на соц сети ГОТОВО - Готово в админке
	-id
	title
	url
	image




-------Модель пользователи и с ним связанные Cart + Orders -------

3. Users наследуемся от BuyerUser ГОТОВО !
	(наследованные поля - username,first_name, last_name, email, is_staff, is_active, date_joined)
	- phone_number - номер телефона
	- user_avatar - аватарка пользователя

4. Carts - корзина покупок ГОТОВО !
	- user - FK на модель user
	- product - FK на модель product
	- quantity - кол-во товара
	- session_key - ключ сессии
	- created  - дата внесения товара в корзину

5. Promo_code - промокод ГОТОВО !
	- id
	- code_value - ключ промокод
	- value_discount - процент скидки
	- created  - дата создания промокода
	- used - дата применения промокода
	- carts_id - к какой корзине покупок применили FK - Carts 
	- user_id - какой пользователь применил
	- is_active - действующий код или нет true false


6. Order - модель заказа ГОТОВО
	- id
	- user - пользователь чей заказ
	- created  - дата создания заказа
	- сustomer - заказчик физ или юр лицо
	- city_ delivery - город получения или адрес доставки
	- method_of_obtaining - способ получения
	- full_name - ФИО
	- phone_number - номер телефона
	- street_name - улица
	- street_number - номер улицы
	- apartment_number -номер квартиры
	- city_index - индекс 
	- payment_cash - метод оплаты (наличка)
	- payment_cart - метод оплаты карта - FK на модель payment_cart  - внося туда данные если да то оплата true
	- status_payment  - статус оплаты(оплачен/ не оплачен)
	- status_delivery  - статус заказа (в обработке, в пути , получен, выполнен)
	- promo_code - промо код

7.Order_item - товары в заказе ГОТОВО
	- id
	- product
	- quantity - кол-во товара
	- session_key - ключ сессии
	- created  - дата внесения товара в корзину

8.Payment_cart  - карта оплаты ГОТОВО
	- id
	- user
	- number_cart
	- date_cart
	- cvv_cart




















		