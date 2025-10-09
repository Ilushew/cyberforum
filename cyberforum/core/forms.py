import uuid

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from .models import User, Event, News, DocumentationFile, EventReport, REPORT_AUDIENCE_CHOICES


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False

        # Генерируем уникальный username из email или UUID
        if not user.username:

            user.username = str(uuid.uuid4())  # гарантирует уникальность

        if commit:
            user.save()
            self.send_confirmation_email(user)
        return user

    def send_confirmation_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_url = f"http://127.0.0.1:8000/confirm-email/{uid}/{token}/"

        subject = "Подтвердите ваш email"
        message = f"""
        Здравствуйте!

        Пожалуйста, подтвердите ваш email, перейдя по ссылке:
        {confirm_url}

        Если вы не регистрировались на сайте, просто проигнорируйте это письмо.
        """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

class UserUpdateForm(UserChangeForm):
    password = None  # Скрыть поле пароля

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone')
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'image', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'audience']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'audience': forms.Select(attrs={'class': 'form-select'}),
        }


class DocumentationFileForm(forms.ModelForm):
    class Meta:
        model = DocumentationFile
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }


from .models import Textbook

class TextbookForm(forms.ModelForm):
    class Meta:
        model = Textbook
        fields = ['title', 'description', 'audience', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'audience': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
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