from django.db import models

AUDIENCE_CHOICES = [
    ("все", "Все"),
    ("школьник", "Школьники"),
    ("пенсионер", "Пенсионеры"),
    ("МСП", "МСП"),
]


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)
    audience = models.CharField(max_length=50, choices=AUDIENCE_CHOICES, default="все")

    def __str__(self):
        return self.title
