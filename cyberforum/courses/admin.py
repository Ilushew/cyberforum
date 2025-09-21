from django.contrib import admin
from .models import Course, Lesson, Question

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'audience', 'format_type', 'created_at']
    list_filter = ['audience', 'format_type']
    search_fields = ['title', 'description']
    inlines = [LessonInline]  # Показывает уроки прямо внутри курса

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    search_fields = ['title', 'content']
    inlines = [QuestionInline]  # Вопросы внутри урока

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'lesson', 'correct_answer']
    list_filter = ['lesson__course']
    search_fields = ['text']