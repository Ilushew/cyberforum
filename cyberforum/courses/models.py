from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

AUDIENCE_CHOICES = [
    ("все", "Все"),
    ("школьник", "Школьники"),
    ("пенсионер", "Пенсионеры"),
    ("МСП", "МСП"),
]

FORMAT_CHOICES = [
    ("текст", "Текст"),
    ("видео", "Видео"),
    ("тест", "Тест"),
]


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    audience = models.CharField(max_length=50, choices=AUDIENCE_CHOICES, default="все")
    format_type = models.CharField(
        max_length=50, choices=FORMAT_CHOICES, default="текст"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)  # YouTube
    order = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Question(models.Model):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="questions"
    )
    text = models.CharField(max_length=300)
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200, blank=True)
    option_d = models.CharField(max_length=200, blank=True)
    correct_answer = models.CharField(max_length=1)  # A, B, C, D

    def __str__(self):
        return self.text


class TestResult(models.Model):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="test_results"
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.PositiveSmallIntegerField()
    total = models.PositiveSmallIntegerField()
    percent = models.PositiveSmallIntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lesson} — {self.percent}%"
