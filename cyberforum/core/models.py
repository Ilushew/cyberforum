from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models
from core.utils import geocode_address


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    email_verified = models.BooleanField(
        default=False, verbose_name="Email подтверждён"
    )
    is_moderator = models.BooleanField(default=False, verbose_name="Модератор")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


AUDIENCE_CHOICES = [
    ("все", "Все"),
    ("школьник", "Школьники"),
    ("пенсионер", "Пенсионеры"),
    ("МСП", "МСП"),
]


class Contact(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    audience = models.CharField(max_length=50, choices=AUDIENCE_CHOICES, default="все")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        lat, lon = geocode_address(self.address)
        self.latitude = lat
        self.longitude = lon
        super().save(*args, **kwargs)


REPORT_AUDIENCE_CHOICES = AUDIENCE_CHOICES + [("другое", "Другое")]


class EventReport(models.Model):
    title = models.CharField("Тема", max_length=200)
    audience = models.CharField(
        "Целевая аудитория", max_length=50, choices=REPORT_AUDIENCE_CHOICES
    )
    custom_audience = models.CharField("Своя аудитория", max_length=100, blank=True)
    listener_count = models.PositiveIntegerField("Количество слушателей")
    date = models.DateField("Дата проведения")
    comments = models.TextField("Комментарии", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    moderator = models.ForeignKey(
        "User", on_delete=models.CASCADE, verbose_name="Модератор"
    )

    class Meta:
        verbose_name = "Отчёт о мероприятии"
        verbose_name_plural = "Отчёты о мероприятиях"
        ordering = ["-date"]

    def __str__(self):
        return self.title

    def get_audience_display(self):
        if self.audience == "другое":
            return self.custom_audience or "Другое"
        return dict(REPORT_AUDIENCE_CHOICES).get(self.audience, self.audience)


class TextbookAdmin(admin.ModelAdmin):
    list_display = ["title", "audience", "file"]
    list_filter = ["audience"]
    search_fields = ["title"]


class Textbook(models.Model):
    AUDIENCE_CHOICES = [
        ("1-4", "Для 1–4 классов"),
        ("5-9", "Для 5–9 классов"),
        ("10-11", "Для 10–11 классов"),
        ("adults", "Для взрослых"),
    ]

    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание", blank=True)
    audience = models.CharField("Аудитория", max_length=10, choices=AUDIENCE_CHOICES)
    file = models.FileField("Файл (PDF/DOCX)", upload_to="textbooks/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Учебник"
        verbose_name_plural = "Учебники"
        ordering = ["audience", "title"]

    def __str__(self):
        return self.title

