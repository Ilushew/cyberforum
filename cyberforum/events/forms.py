from django import forms

from core.models import EventReport
from events.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "date", "location", "audience"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "audience": forms.Select(attrs={"class": "form-select"}),
        }

class EventReportForm(forms.ModelForm):
    # Поле для выбора существующего мероприятия (опционально)
    existing_event = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        label="Выбрать тему из существующих мероприятий",
        required=False,
        empty_label="— Не выбрано —",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_existing_event'})
    )
    # Поле для ручного ввода темы
    manual_title = forms.CharField(
        label="Или введите новую тему",
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_manual_title'})
    )

    class Meta:
        model = EventReport
        fields = ['audience', 'custom_audience', 'listener_count', 'date', 'comments']
        widgets = {
            'audience': forms.Select(attrs={'class': 'form-select', 'id': 'id_audience'}),
            'custom_audience': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: студенты колледжей'}),
            'listener_count': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Дополнительные замечания (необязательно)'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        existing_event = cleaned_data.get('existing_event')
        manual_title = cleaned_data.get('manual_title')
        audience = cleaned_data.get('audience')
        custom_audience = cleaned_data.get('custom_audience')

        # Валидация темы
        if not existing_event and not manual_title:
            raise forms.ValidationError("Укажите тему: выберите из списка или введите вручную.")
        if existing_event and manual_title:
            raise forms.ValidationError("Выберите ТОЛЬКО один способ указания темы.")

        # Валидация аудитории
        if audience == 'другое' and not custom_audience:
            raise forms.ValidationError("Пожалуйста, укажите свою целевую аудиторию.")
        if audience != 'другое' and custom_audience:
            raise forms.ValidationError("Поле «Своя аудитория» нужно заполнять только при выборе «Другое».")

        # Установка title
        if existing_event:
            cleaned_data['title'] = existing_event.title
        else:
            cleaned_data['title'] = manual_title

        return cleaned_data

    def save(self, commit=True, moderator=None):
        instance = super().save(commit=False)
        instance.title = self.cleaned_data['title']
        if moderator:
            instance.moderator = moderator
        if commit:
            instance.save()
        return instance