from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from users.models import UserBuyersData


#Форма регистрации пользователя на базе UserCreationForm
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-input', "placeholder": "Логин"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-input', "placeholder": "Имя"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-input', "placeholder": "Фамилия"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-input', "placeholder": "Введите ваш пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-input', "placeholder": "Повторите ваш пароль"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-input', "placeholder": "Ваш E-mail",}))
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name','password1', 'password2', 'email']


#Форма авторизации пользователя на базе AuthenticationForm
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input', "placeholder": "Логин"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', "placeholder": "Введите ваш пароль"}))

    class Meta:
        model = User
        fields = ['username', 'password']

#Форма востановления пароля
class NewPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-input', "placeholder": "Ваша электронная почта",}))

#Форма редактирования профиля пользователя модель - UserBuyersData
class UserBuyersDataRedactor(forms.ModelForm):
    class Meta:
        model = UserBuyersData
        fields = ['nick_name', 'image', 'phone_number']
        labels = {
            'nick_name': 'Логин', 'image':'Аватарка', 'phone_number':'Номер телефона'
        }
        widgets = {
            'nick_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'nick_name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'phone_number'}),
        }
