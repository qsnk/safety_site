from django import forms
class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={
        'placeholder': 'Введите имя пользователя',
        'class': 'form-control'
    }))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль',
        'class': 'form-control'
    }))