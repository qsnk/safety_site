from django import forms
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя", required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Введите имя пользователя',
        'class': 'form-control'
    }))
    email = forms.CharField(label="Электронная почта", required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Введите электронную почту',
        'class': 'form-control'
    }))
    password1 = forms.CharField(label="Пароль", required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль',
        'class': 'form-control'
    }))
    password2 = forms.CharField(label="Повторите пароль", required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'Повторите пароль',
        'class': 'form-control'
    }))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя", required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Введите имя пользователя',
        'class': 'form-control'
    }))
    password = forms.CharField(label="Пароль", required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль',
        'class': 'form-control'
    }))