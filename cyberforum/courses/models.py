from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    audience = models.CharField(max_length=50)  # школьник, пенсионер, МСП
    format_type = models.CharField(max_length=50)  # текст, видео, тест
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)  # YouTube
    order = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=300)
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200, blank=True)
    option_d = models.CharField(max_length=200, blank=True)
    correct_answer = models.CharField(max_length=1)  # A, B, C, D

    def __str__(self):
        return self.text