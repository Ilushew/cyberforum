from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Lesson, Question, TestResult


def course_list_view(request):
    courses = Course.objects.all()

    # Получаем параметры фильтрации
    audience = request.GET.get('audience')
    format_type = request.GET.get('format')

    if audience:
        courses = courses.filter(audience=audience)
    if format_type:
        courses = courses.filter(format_type=format_type)

    return render(request, 'courses/list.html', {'courses': courses})


def course_detail_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/detail.html', {'course': course})


def lesson_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.questions.all()
    return render(request, 'courses/lesson.html', {
        'lesson': lesson,
        'questions': questions,
    })


def submit_test_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.questions.all()
    total = questions.count()
    correct = 0
    if request.method == "POST":
        for q in questions:
            user_answer = request.POST.get(f'q{q.id}')
            if user_answer == q.correct_answer:
                correct += 1
        score_percent = int((correct / total) * 100) if total > 0 else 0

        # Сохраняем результат
        TestResult.objects.create(
            lesson=lesson,
            user=request.user if request.user.is_authenticated else None,
            score=correct,
            total=total,
            percent=score_percent
        )

        return render(request, 'courses/result.html', {
            'score': correct,
            'total': total,
            'percent': score_percent,
            'lesson': lesson,
        })
    return redirect('courses:lesson', lesson_id=lesson_id)
