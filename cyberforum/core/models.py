from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    audience = models.CharField(max_length=50)  # все, школьники, пенсионеры

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)
    audience = models.CharField(max_length=50)

    def __str__(self):
        return self.title