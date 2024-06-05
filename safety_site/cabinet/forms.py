from django import forms
from cabinet.models import Place, Camera, Violation, Report


class AddCameraForm(forms.Form):
    name = forms.CharField(label="Подпись камеры", required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Введите подпись для камеры',
        'class': 'form-control'
    }))
    url = forms.CharField(label="Ссылка для подключения", required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Введите ссылку для подключения к камере',
        'class': 'form-control'
    }))


class AddPlaceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        super(AddPlaceForm, self).__init__(*args, **kwargs)
        self.fields['camera_id'].queryset = Camera.objects.filter(user_id=user_id)

    name = forms.CharField(label="Подпись участка", required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Введите подпись для участка',
        'class': 'form-control'
    }))
    description = forms.CharField(label="Описание участка", required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Введите описание для участка',
        'class': 'form-control'
    }))
    camera_id = forms.ModelChoiceField(label="Камера участка", required=True, queryset=Camera.objects.none())


class ShowPlaceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        super(ShowPlaceForm, self).__init__(*args, **kwargs)
        self.fields['places'].queryset = Place.objects.filter(user_id=user_id)
    places = forms.ModelMultipleChoiceField(label='Площадки', required=False, queryset=Place.objects.none(), widget=forms.CheckboxSelectMultiple(attrs={}))


class FilterJournalForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        super(FilterJournalForm, self).__init__(*args, **kwargs)
        self.fields['violations'].choices = [(violation.violation_class, violation.violation_class) for violation in Violation.objects.filter(user_id=user_id).order_by('violation_class').distinct('violation_class')]
    date_start = forms.DateField(label='[дата] от', required=False, widget=forms.DateInput(attrs={
        'class': 'form-control',
        'type': 'date'
    }))
    date_end = forms.DateField(label='[дата] до',required=False, widget=forms.DateInput(attrs={
        'class': 'form-control',
        'type': 'date'
    }))
    time = forms.TimeField(label='Время', required=False, widget=forms.TimeInput(attrs={
        'class': 'form-control',
        'type': 'time'
    }))
    violations = forms.MultipleChoiceField(label='Класс нарушения', required=False,
                                           choices=[],
                                           widget=forms.CheckboxSelectMultiple(attrs={'type': 'checkbox'
    }))


class AddReportForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        super(AddReportForm, self).__init__(*args, **kwargs)
        self.fields['violation'].queryset = Violation.objects.filter(user_id=user_id)

    name = forms.CharField(label="Название отчета", required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text'
    }))
    violation = forms.ModelChoiceField(label="Нарушение", required=True, queryset=Violation.objects.none(), widget=forms.Select(attrs={
        'class': 'form-control'
    }))


class FilterReportForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        super(FilterReportForm, self).__init__(*args, **kwargs)
        self.fields['violations'].choices = [(violation.violation_class, violation.violation_class) for violation in Violation.objects.filter(user_id=user_id).order_by('violation_class').distinct('violation_class')]
    date_start = forms.DateField(label='[дата] от', required=False, widget=forms.DateInput(attrs={
        'class': 'form-control',
        'type': 'date'
    }))
    date_end = forms.DateField(label='[дата] до', required=False, widget=forms.DateInput(attrs={
        'class': 'form-control',
        'type': 'date'
    }))
    time = forms.TimeField(label='Время', required=False, widget=forms.TimeInput(attrs={
        'class': 'form-control',
        'type': 'time'
    }))
    violations = forms.MultipleChoiceField(label='Класс нарушения', required=False,
                                               choices=[],
                                                widget=forms.CheckboxSelectMultiple(attrs={'type': 'checkbox'
    }))
