/*Эффект - из nav меню открыть список ссылок, переворот стрелки - открыть список категорий в мобильном меню */
let rotateLine = 180;
let statusMobileMenuList = [
	'close',
	'open',
];
let statusMobileMenu = statusMobileMenuList[0];
$(".list_of_goods").click(
	
	function(){
		if (statusMobileMenu != 'open'){
			$('.list_of_category').css('display','block');
			rotateLine +=180;
			$(".nav_item_arrow").css({ transform: "rotate(" + rotateLine + "deg" })
			statusMobileMenu = statusMobileMenuList[1];
		}
		else if (statusMobileMenu != 'close') {
			$('.list_of_category').css('display', 'none');
			rotateLine += 180;
			$(".nav_item_arrow").css({ transform: "rotate(" + rotateLine + "deg" })
			statusMobileMenu = statusMobileMenuList[0];
		}
	}
)

/*Автоматический слайдер в шапке сайта на 3 фотографии - переключение каждые 5 сек */
let sliderList = [
	'static/images/header/slider_header/first_slide.png',
	'static/images/header/slider_header/second_slide.png',
	'static/images/header/slider_header/thirt_slide.png'
]

let sliderCounter = 0;

const intervalId = setInterval(function changeSliderPhoto() {
	if (sliderCounter >= -1 && sliderCounter < 2) {
		sliderCounter += 1;
		$('.header_slider_img').attr("src", sliderList[sliderCounter]);
		$(`.slider_indicator:eq(${sliderCounter})`).toggleClass('slider_indicator_orange');
		$(`.slider_indicator:not(:eq(${sliderCounter}))`).removeClass('slider_indicator_orange');
	}
	else return sliderCounter = -1;
}, 4000)


/*Загрузка и смена img - кнопка ссылка на корзину при смене ширины экрана */
$(document).ready(function () {
	if (window.innerWidth > 576) {
		$('.cart_img').attr('src','/static/images/header/cart.svg')}
	else if (window.innerWidth <= 576) {
		$('.cart_img').attr('src', '/static/images/header/cart_white.svg')
	}
	})

let imgSelect = [
	'/static/images/header/cart.svg',
	'/static/images/header/cart_white.svg',
];

$(window).resize(function (){
	if (window.innerWidth > 576) {
		$('.cart_img').attr('src', '/static/images/header/cart.svg')
	}
	else if (window.innerWidth <= 576) {
		$('.cart_img').attr('src', '/static/images/header/cart_white.svg')
	}
})

/*Открыть закрыть мобильное меню*/

	let statusMenuList = ['close','open'];
	let statusMenu = statusMenuList[0];

	let statusFormList = ['close', 'open'];
	let statusForm = statusFormList[0];

$('.nav_menu').on('click', function openMenu(e){
		//открываем
	if (statusMenu != 'open'){
		statusMenu = statusMenuList[1];
		$('.header_block_container').css('height', 540 + 'px')
		$('.block_logo').css('padding-top',60+'px');
		$('.nav_menu_img').attr('src','/static/images/header/ic-close-menu.svg');
		$('.photo_slider_block').css('visibility', 'hidden');
		$('.nav_block_data').css('visibility', 'visible');

		//По умолчанию скрываем форму поиска - даже если она не открыта и ставим статус - закрыто
		statusForm = statusFormList[0];
		$('.form_seach_site').css('visibility', 'hidden')
	}
	//закрываем
	else if ( statusMenu == 'open') {
		statusMenu = statusMenuList[0];
		$('.header_block_container').css('height', 'auto')
		$('.block_logo').css('padding-top', 11 + 'px');
		$('.nav_menu_img').attr('src', '/static/images/header/nav_menu_open.svg');
		$('.photo_slider_block').css('visibility', 'visible');
		$('.nav_block_data').css('visibility', 'hidden')

		//По умолчанию скрываем форму поиска - даже если она не открыта и ставим статус - закрыто
		statusForm = statusFormList[0];
		$('.form_seach_site').css('visibility', 'hidden')
	}
})


/*Открываем форму поиска - мобильный дисплей - data_seach_btn_2 */
	
$(".data_seach_btn_2").on('click', function(e){
	if (statusForm != 'open') {
		statusForm = statusFormList[1];
		$('.block_logo').css('padding-top', 11 + 'px');
		$('.photo_slider_block').css('visibility', 'hidden')
		$('.form_seach_site').css('visibility', 'visible')

		//По умолчанию скрываем мобильное меню - даже если она не открыта и ставим статус - закрыто
		statusMenu = statusMenuList[0];
		$('.nav_block_data').css('visibility', 'hidden')
	}
	else if (statusForm == 'open') {
		statusForm = statusFormList[0];
		$('.form_seach_site').css('visibility', 'hidden')
		$('.nav_menu_img').attr('src', '/static/images/header/nav_menu_open.svg');
		$('.photo_slider_block').css('visibility', 'visible');

		//По умолчанию скрываем мобильное меню - даже если она не открыта и ставим статус - закрыто
		statusMenu = statusMenuList[0];
		$('.nav_block_data').css('visibility', 'hidden')
	}
});
//Закрываем форму по кнопке отмена в форме
$('.btn_close_form').on('click', function(e){
	if (statusForm == 'open') {
		statusForm = statusFormList[0];
		$('.form_seach_site').css('visibility', 'hidden')
		$('.nav_menu_img').attr('src', '/static/images/header/nav_menu_open.svg');
		$('.photo_slider_block').css('visibility', 'visible');

		//По умолчанию скрываем мобильное меню - даже если она не открыта и ставим статус - закрыто
		statusMenu = statusMenuList[0];
		$('.nav_block_data').css('visibility', 'hidden')
	}
})

/*Открываем форму поиска - desctop дисплей - data_seach_btn - через toggleclass */
$('.data_seach_btn').on('click', function(e){
	$('.form_seach_site').toggleClass('form_seach_site_desc');
	$('.form_seach').toggleClass('form_seach_desc');
	$('.form_header').toggleClass('form_header_desc');
	$('.form_seach_buttons').toggleClass('form_seach_buttons_desc');
	$('.btn_close_form').toggleClass('btn_close_form_desc');
	$('.seach').toggleClass('seach_desc');
	$('main').toggleClass('main_opasity')
})



/*Скрипты для страницы - Catalog of Goods------------------------*/
//Открыть/скрыть панель меню - catalog_of_goods

let listCatalogVisible = ['close', 'open',];
let catalogVisibleStatus = listCatalogVisible[0];

$(".nav_item_btn_big").on('click', function(e){
	$('.nav_item_arrow_big').css('rotate','+=180deg')
	if (catalogVisibleStatus != 'open'){
		catalogVisibleStatus = listCatalogVisible[1]
		$('.catalog_of_goods').css('display','flex');
		$('main').addClass('main_opasity')
	}
	else if (catalogVisibleStatus == 'open') {
		catalogVisibleStatus = listCatalogVisible[0]
		$('.catalog_of_goods').css('display', 'none')
		$('main').removeClass('main_opasity')
	}
})





