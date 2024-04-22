const cityList = [
	{ Id: 1, Name: 'Адыгейск' },
	{ Id: 2, Name: 'Майкоп' },
	{ Id: 3, Name: 'Горно-Алтайск' },
	{ Id: 4, Name: 'Углич' },
	{ Id: 5, Name: 'Ярославль' },
	{ Id: 6, Name: 'Нижний Новгород' },
	{ Id: 7, Name: 'Нижний Тагил' },
	{ Id: 8, Name: 'Нижневартовск' },
	{ Id: 9, Name: 'Нижнекамск' },
];
/*Работа с формой заказа */

//открываем-скрываем  инпут (поле, кнопки, радио или чек боксы)
$('.header_form_item, .order_form_item adres_list').on('click', function (e) {
	//Открыть инпуты в формах
	let a = $(this).siblings('.item_body')
	a.slideToggle()

	//Открыть блок инпутов при доставке почтой или курьером
	let b = $(this).siblings('.courier_or_post_delivery')
	$(b).children('.item_body').slideToggle()

	//Открыть блок инпутов при доставке через постамат
	let p = $(this).siblings('.postamat_delivery')
	$(p).slideToggle()
	console.log('hgf')
})

//Делаем radio - checked - для блок с чекбоксом
$('.item_body').on('click', function (e) {
	//ищем радио , очищаем от чекед а затем делаем чекед тому на кого клик
	let radioList = $(this).find('.radio_data')
	radioList.map((r) => $(radioList[r]).removeAttr('checked'))
	if (e.target.className == 'radio_data') {
		$(e.target).attr('checked', 'true')
		let e_target_parent = $(this).parent('.order_form_item')
		//ищем родителя для смены стиля
		let radioData = $(e_target_parent).find('.radio_data:checked')
		if (radioData) {
			$(e_target_parent).addClass('order_form_item_checked')
			$(e_target_parent).find('.checked_item_form').addClass('checked_item_form_checked')
		}
	}
})

//Обработка вариантов доставки товара

//HTML форм для адресов доставки
let courier_or_post = `<div class="courier_or_post_delivery">
	<div class="item_body">
		<input type="text" id="full_name" class="form_imput_adress full_name" placeholder="ФИО получателя" value="" />
	</div>
	<div class="item_body">
		<label for="tell" class="label_block">+7</label>
		<input type="tel" id="tell" name="tell" class="form_imput_tell phone" placeholder="Телефон" value="" />
	</div>
	<div class="item_body">
		<input type="text" id="street" name="street" class="form_imput_street street" placeholder="Улица" value="" />
	</div>
	<div class="item_body">
		<div class="item_body_flex">
			<input type="text" id="ind_city" name="ind_city" class="form_imput_street ind_city" placeholder="Индекс" value="" />
			<input type="text" id="home" name="home" class="form_imput_street home" placeholder="Дом" value="" />
			<input type="text" id="flat" name="flat" class="form_imput_street flat" placeholder="Квартира" value="" />
		</div>
	</div>
</div>`

let postamat = `<div class="postamat_delivery">
									<div class="street_seach_block">
										<input type="text" id="map_street" name="map_street" class="map_street" placeholder="Улица  или станция метро" value="" />
										<button class="seach_street_btn" value='1'>

										</button>
									</div>
									<img src="./link/img/order_detail/Mask Group.svg" alt="Карта" class="map_block">
								</div>`

// 1 Если Курьерская или почта то блок courier_or_post_delivery 
$('input[value=delivery_self] , input[value=post_rus]').on('click', function (e) {
	let target = e.target
	if (target['checked'] == true) {
		$('.adres_list').children('.courier_or_post_delivery , .postamat_delivery').empty()
		$('.adres_list').append(
			courier_or_post
		)
	}
})

// 2 Если постамат то блок postamat_delivery 
$('input[value=postamat]').on('click', function (e) {
	let target = e.target
	if (target['checked'] == true) {
		$('.adres_list').children('.courier_or_post_delivery , .postamat_delivery').empty()
		$('.adres_list').append(
			postamat
		)
	}
})


//Обработка inputa с выбром (город улица и тд) и меняем стиль для родителя
//Настройки для выбора города из инпута
$('#city').autocomplete({
	dataSource: cityList,
	valueProperty: 'Id',
	textProperty: 'Name',
	allowCustomValue: true
});

$('.form_imput_order').on('mouseenter, mouseleave', function (e) {
	let input_elem = $(e.target)
	let input_elem_len = input_elem.val().length
	if (input_elem_len > 0) {
		$(e.target).closest('.order_form_item').addClass('order_form_item_checked').find('.checked_item_form').addClass('checked_item_form_checked')
	}
	else {
		$(e.target).closest('.order_form_item').removeClass('order_form_item_checked').find('.checked_item_form').removeClass('checked_item_form_checked')
	}
})

//Блок с инпутами адрес доставки - стилизация если все инпуты отмечены
$('.adres_list').mouseenter(function (e) {

	let list_input_elem = []
	let input_list = $('.adres_list').find(':input')
	for (let input_item = 0; input_item < input_list.length; input_item++) {
		let elem = $(input_list[input_item])

		list_input_elem.push(elem.val().length)
	}
	if (list_input_elem.includes(0) == false && list_input_elem.length > 0) {
		$('.adres_list').closest('.order_form_item').addClass('order_form_item_checked').find('.checked_item_form').addClass('checked_item_form_checked')
	}
	else if (list_input_elem.includes(0) == true) {
		$('.adres_list').closest('.order_form_item').removeClass('order_form_item_checked').find('.checked_item_form').removeClass('checked_item_form_checked')
	}
})

/*Часть формы с формой оплаты и табсами */

$('input[name="pay_type"]').on('click', function (e) {
	let tabs_list = $('.tabs_block').children()
	let e_data = $(e.target).attr("data-tabs-btn")
	for (let tab = 0; tab < tabs_list.length; tab++) {
		if (e_data === $(tabs_list[tab]).attr('data-tabs')) {
			$(tabs_list[tab]).show()
		}
		else if (e_data != $(tabs_list[tab]).attr('data-tabs')) {
			$(tabs_list[tab]).hide()
		}
	}
})

//4 инпута номер карты
$('.input_mask_number').click(function (e) {
	$(this).children('.cart_p_14').css('display', 'none')
	$(this).children('.cart_number').css('display', 'block')
})
//2 инпут - дата карты
$('.input_mask_date').click(function (e) {
	$(this).children('.cart_p_14').css('display', 'none')
	$(this).children('.cart_date').css('display', 'block')
	$(this).children('.between_span').css('display', 'block')
})

/*Блок вариант оплаты - смена стиля если все данные заполнены */
$('#payment_type').on('click keydown', function (e) {
	let classStyleList = ['radio_data pay_data',]
	let variants_list = $('.variant_pay').find(':input[name=pay_type]')
	//console.log(variants_list,'Список вариантов', typeof(variants_list))
	if (classStyleList.includes(e.target.className)) {
		for (let i = 0; i < variants_list.length; i++) {
			if (variants_list[i]['value'] == $(e.target).val()) {
				$(e.target).attr('checked', 'true')
			}

		}
	}
	if ($('#pay_type_cash').attr('checked')) {
		$('#payment_type').addClass('order_form_item_checked')
		$('#payment_type').find('.checked_item_form ').addClass('checked_item_form_checked')
	}

	else if ($('#pay_type_bank_cart').attr('checked')) {
		let input_list = $('.bank_cart_tabs').find('input')
		$($('.bank_cart_tabs').find('input')).on('keydown', function () {
			let input_list_len = []
			input_list.map((e) => {
				input_list_len.push($(input_list[e]).val().length)
			})

			if (input_list_len.includes(0) == false) {
				$('#payment_type').addClass('order_form_item_checked')
				$('#payment_type').find('.checked_item_form').addClass('checked_item_form_checked')
			}
			else if (input_list_len.includes(0) == true) {
				$('#payment_type').removeClass('order_form_item_checked')
				$('#payment_type').find('.checked_item_form').removeClass('checked_item_form_checked')
			}
		})
	}
	else if ($('#pay_type_tinkoff').attr('checked')) {
		$('#tinkoff_cart_tab').children('input').on('keydown', function (e) {
			if ($('#tinkoff_cart_tab').children('input').val().length > 0) {
				$('#payment_type').addClass('order_form_item_checked')
				$('#payment_type').find('.checked_item_form').addClass('checked_item_form_checked')
			}
			else if ($('#tinkoff_cart_tab').children('input').val().length < 1) {
				$('#payment_type').removeClass('order_form_item_checked')
				$('#payment_type').find('.checked_item_form').removeClass('checked_item_form_checked')
			}
		})
	}
})
$('.take_order_form').on('click', function () {
	if ($('.take_order_form').find('.order_form_item_checked').length == 5) {
		$('.take_order_form').find('.order_btn_orange').removeAttr('disabled')
	}
	else {
		$('.take_order_form').find('.order_btn_orange').attr('disabled', true)
	}
})
