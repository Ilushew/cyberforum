# courses/utils.py
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Question, CourseCompletion, TestResult

User = get_user_model()


def mark_course_as_completed(user, course):
    if not user.is_authenticated:
        return

    # Получаем все уроки курса, которые содержат вопросы (тесты)
    lessons_with_questions = Lesson.objects.filter(
        course=course,
        questions__isnull=False
    ).distinct()

    if not lessons_with_questions.exists():
        # Нет уроков с тестами → курс считается пройденным
        CourseCompletion.objects.get_or_create(user=user, course=course)
    else:
        # Получаем ID уроков с тестами
        required_lesson_ids = set(lessons_with_questions.values_list('id', flat=True))

        # Получаем ID уроков, по которым пользователь уже прошёл тест
        completed_lesson_ids = set(
            TestResult.objects.filter(
                user=user,
                lesson__course=course,
                lesson__in=required_lesson_ids
            ).values_list('lesson_id', flat=True)
        )

        if completed_lesson_ids == required_lesson_ids:
            CourseCompletion.objects.get_or_create(user=user, course=course)
