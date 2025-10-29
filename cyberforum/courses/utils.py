import courses.models

from django.contrib.auth import get_user_model


User = get_user_model()


def mark_course_as_completed(user, course):
    if not user.is_authenticated:
        return

    lessons_with_questions = courses.models.Lesson.objects.filter(
        course=course, questions__isnull=False
    ).distinct()

    if not lessons_with_questions.exists():
        courses.models.CourseCompletion.objects.get_or_create(user=user, course=course)
    else:
        required_lesson_ids = set(lessons_with_questions.values_list("id", flat=True))

        completed_lesson_ids = set(
            courses.models.TestResult.objects.filter(
                user=user, lesson__course=course, lesson__in=required_lesson_ids
            ).values_list("lesson_id", flat=True)
        )

        if completed_lesson_ids == required_lesson_ids:
            courses.models.CourseCompletion.objects.get_or_create(user=user, course=course)
