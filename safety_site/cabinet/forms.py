from django import forms
from cabinet.models import Place, Camera


class AddCameraForm(forms.Form):
    name = forms.CharField(label="Подпись камеры", widget=forms.TextInput(attrs={
        'placeholder': 'Введите подпись для камеры',
        'class': 'form-control'
    }))
    url = forms.CharField(label="Ссылка для подключения", widget=forms.TextInput(attrs={
        'placeholder': 'Введите ссылку для подключения к камере',
        'class': 'form-control'
    }))


class AddPlaceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        super(AddPlaceForm, self).__init__(*args, **kwargs)
        self.fields['camera_id'].queryset = Camera.objects.filter(user_id=user_id)

    name = forms.CharField(label="Подпись участка", widget=forms.TextInput(attrs={
        'placeholder': 'Введите подпись для участка',
        'class': 'form-control'
    }))
    description = forms.CharField(label="Описание участка", required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Введите описание для участка',
        'class': 'form-control'
    }))
    camera_id = forms.ModelChoiceField(label="Камера участка", queryset=Camera.objects.none())


class ShowPlaceForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        super(ShowPlaceForm, self).__init__(*args, **kwargs)
        self.fields['places'].choices = Place.objects.filter(user_id=user_id)

    places = forms.ChoiceField(label="Выберите участок", choices=Place.objects.none(), widget=forms.CheckboxInput())