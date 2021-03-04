from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин:',
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Логин'},),
    )
    password = forms.CharField(
        label='Пароль:',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'})
    )

    error_messages = {
        'invalid_login': "Пожалуйста, введите правильное имя пользователя и пароль. Учтите что оба поля могут быть "
                         "чувствительны к регистру.",
        'inactive': "Не активирована почта или произошла техническая ошибка.",
    }


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Логин:',
        required=True,
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Логин'}),
    )
    email = forms.EmailField(
        label='Email:',
        required=True,
        help_text="Введите правильный email.",
        widget=forms.TextInput(attrs={'placeholder': 'Email'})
    )
    password1 = forms.CharField(
        label='Пароль:',
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
    )
    password2 = forms.CharField(
        label='Повторите пароль:',
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}),
    )

    error_messages = {
        'password_mismatch': 'Поля ввода паролей не совпадают.',
    }

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
