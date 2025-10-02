from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    email_verified = models.BooleanField(default=False, verbose_name="Email подтверждён")

    USERNAME_FIELD = 'email'  # Используем email для входа
    REQUIRED_FIELDS = ['username']      # Не требуем другие поля при создании через createsuperuser

    def __str__(self):
        return self.email


AUDIENCE_CHOICES = [
    ('все', 'Все'),
    ('школьник', 'Школьники'),
    ('пенсионер', 'Пенсионеры'),
    ('МСП', 'МСП'),
]

class Contact(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    audience = models.CharField(max_length=50, choices=AUDIENCE_CHOICES, default='все')

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)
    audience = models.CharField(max_length=50, choices=AUDIENCE_CHOICES, default='все')

    def __str__(self):
        return self.title
