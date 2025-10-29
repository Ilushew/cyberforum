import core.utils

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
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.location and (not self.latitude or not self.longitude):
            lat, lon = core.utils.geocode_address(self.location)
            self.latitude = lat
            self.longitude = lon
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
