from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, ListView, DetailView, CreateView, FormView
from users.forms import RegisterUserForm, LoginUserForm
from django.contrib.messages.views import SuccessMessageMixin
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