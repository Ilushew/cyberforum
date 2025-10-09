from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from .utils import geocode_address

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    email_verified = models.BooleanField(default=False, verbose_name="Email подтверждён")
    is_moderator = models.BooleanField(default=False, verbose_name="Модератор")

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
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    audience = models.CharField(max_length=50, choices=AUDIENCE_CHOICES, default='все')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        lat, lon = geocode_address(self.address)
        self.latitude = lat
        self.longitude = lon
        super().save(*args, **kwargs)

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)
    audience = models.CharField(max_length=50, choices=AUDIENCE_CHOICES, default='все')

    def __str__(self):
        return self.title

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    image = models.ImageField(
        upload_to='news_images/',
        blank=True,
        null=True,
        verbose_name="Изображение"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    author = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'is_moderator': True},
        verbose_name="Автор"
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']

    def __str__(self):
        return self.title