from django import forms
class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя", required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Введите имя пользователя',
        'class': 'form-control'
    }))
    password = forms.CharField(label="Пароль", required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль',
        'class': 'form-control'
    }))