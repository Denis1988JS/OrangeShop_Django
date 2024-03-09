from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, ListView, DetailView, CreateView, FormView
from users.forms import RegisterUserForm, LoginUserForm, NewPasswordForm
from django.contrib import messages

import string
import random



#Функция генерирует пароль
def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(8))
    return password

# Create your views here.

#Регистрация пользователя
class RegisterUser(CreateView):
    template_name = 'users/registration.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('home')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

#Авторизация пользователя
class LoginUser(LoginView):
    template_name = 'users/login.html'
    form_class = LoginUserForm
    success_url = reverse_lazy('home')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Страница авторизации пользователя'
        return context
    def get_success_url(self):
        return reverse_lazy('home')

#Напомнить пароль

class NewPassword(TemplateView):
    template_name =  'users/new_password.html'
    def post(self, request):
        form = NewPasswordForm(request.POST)
        user_email = request.POST['email']
        try:
            user = User.objects.get(Q(email=user_email))
            if user:
                print(user)
                generated_password = generate_password()
                user.password = generated_password
                print(user.password)
                user.save()
                #Ниже отправка e-mail - код при тесте был рабочий - чтобы не светить почту код закомментирован
                # message_data = f'Ваш новый пароль - {generated_password}'
                # em = EmailMessage(
                #     subject='Ваш новый пароль',
                #     body=message_data,
                #     to=[f'{user_email} ']
                # )
                # em.send()
                messages.success(request, f'Вам отправлено письмо на {user_email}  с новым паролем')
                return redirect('login')

        except User.DoesNotExist :
                print(f'По введенному имени почты {user_email}  пользователь не найден!!!')
                messages.error(request, f'По введенному имени почты {user_email}  пользователь не найден!!!')
                return redirect('new_pass')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Страница востановления пароля'
        context['form'] = NewPasswordForm
        return context