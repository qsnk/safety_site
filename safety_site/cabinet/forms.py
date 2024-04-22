from django import forms
class AddCameraForm(forms.Form):
    name = forms.CharField(label="Подпись камеры", widget=forms.TextInput(attrs={
        'placeholder': 'Введите подпись для камеры',
        'class': 'form-control'
    }))
    url = forms.CharField(label="Ссылка для подключения", widget=forms.TextInput(attrs={
        'placeholder': 'Введите ссылку для подключения к камере',
        'class': 'form-control'
    }))