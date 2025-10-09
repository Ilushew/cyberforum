from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from .utils import geocode_address


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    email_verified = models.BooleanField(
        default=False, verbose_name="Email подтверждён"
    )
    is_moderator = models.BooleanField(default=False, verbose_name="Модератор")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username"
    ]

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
