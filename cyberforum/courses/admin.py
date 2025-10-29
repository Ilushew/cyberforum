import courses.models

from django.contrib import admin


class LessonInline(admin.TabularInline):
    model = courses.models.Lesson
    extra = 1


class QuestionInline(admin.TabularInline):
    model = courses.models.Question
    extra = 1


@admin.register(courses.models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "audience", "format_type", "created_at"]
    list_filter = ["audience", "format_type"]
    search_fields = ["title", "description"]
    inlines = [LessonInline]


@admin.register(courses.models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "order"]
    list_filter = ["course"]
    search_fields = ["title", "content"]
    inlines = [QuestionInline]


@admin.register(courses.models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["text", "lesson", "correct_answer"]
    list_filter = ["lesson__course"]
    search_fields = ["text"]
