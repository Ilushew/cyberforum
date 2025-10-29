import uuid
import core.models

from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = core.models.User
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False

        if not user.username:
            user.username = str(uuid.uuid4())

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
    password = None

    class Meta:
        model = core.models.User
        fields = ("username", "first_name", "last_name", "email", "phone")
        widgets = {
            "username": forms.TextInput(attrs={"readonly": "readonly"}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = core.models.User
        fields = ("first_name", "last_name", "phone")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }


class TextbookForm(forms.ModelForm):
    class Meta:
        model = core.models.Textbook
        fields = ["title", "description", "audience", "file"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "audience": forms.Select(attrs={"class": "form-select"}),
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
