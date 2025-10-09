import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
import io
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit
from reportlab.lib.colors import Color
from django.contrib import messages
from .models import Course, Lesson, Question, TestResult, CourseCompletion
from .utils import mark_course_as_completed
from cyberforum import settings


def course_list_view(request):
    courses = Course.objects.all()

    # Получаем параметры фильтрации
    audience = request.GET.get("audience")
    format_type = request.GET.get("format")

    if audience:
        courses = courses.filter(audience=audience)
    if format_type:
        courses = courses.filter(format_type=format_type)

    return render(request, "courses/list.html", {"courses": courses})


def course_detail_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, "courses/detail.html", {"course": course})


def lesson_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.questions.all()

    # 🔥 Если урока нет теста — всё равно проверяем, можно ли засчитать курс
    if request.user.is_authenticated and not questions.exists():
        mark_course_as_completed(request.user, lesson.course)

    return render(request, 'courses/lesson.html', {
        'lesson': lesson,
        'questions': questions,
    })


def submit_test_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.course
    questions = lesson.questions.all()
    total = questions.count()
    correct = 0
    if request.method == "POST":
        for q in questions:
            user_answer = request.POST.get(f"q{q.id}")
            if user_answer == q.correct_answer:
                correct += 1
        score_percent = int((correct / total) * 100) if total > 0 else 0

        TestResult.objects.create(
            lesson=lesson,
            user=request.user if request.user.is_authenticated else None,
            score=correct,
            total=total,
            percent=score_percent,
        )

        # 🔥 Помечаем курс как пройденный (если условия выполнены)
        if request.user.is_authenticated:
            mark_course_as_completed(request.user, course)

        return render(request, 'courses/result.html', {
            'score': correct,
            'total': total,
            'percent': score_percent,
            'lesson': lesson,
        })
    return redirect('courses:lesson', lesson_id=lesson_id)




@login_required
def download_certificate(request, course_id):
    completion = get_object_or_404(
        CourseCompletion,
        user=request.user,
        course_id=course_id
    )

    if not (request.user.first_name and request.user.last_name):
        messages.error(
            request,
            "Для получения сертификата необходимо указать имя и фамилию в личном кабинете."
        )
        return redirect('core:profile')

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # === ЦВЕТА ===
    primary_color = Color(106/255, 125/255, 93/255)      # #6a7d5d
    bg_color = Color(248/255, 246/255, 240/255)          # #f8f6f0
    text_color = Color(0.2, 0.2, 0.2)                    # тёмно-серый
    light_border = Color(106/255, 125/255, 93/255, alpha=0.1)

    # === ШРИФТ ===
    font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'DejaVuSans.ttf')
    try:
        pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
        font_name = 'DejaVuSans'
    except Exception as e:
        print(f"⚠️ Шрифт не найден: {e}")
        font_name = 'Helvetica'

    # === ФОН ===
    p.setFillColor(bg_color)
    p.rect(0, 0, width, height, stroke=0, fill=1)

    # === ДЕКОРАТИВНАЯ ВЕРХНЯЯ ПОЛОСА ===
    p.setFillColor(primary_color)
    p.rect(0, height - 90, width, 90, stroke=0, fill=1)

    # === ЗАГОЛОВОК ===
    p.setFont(font_name, 28)
    p.setFillColor(Color(1, 1, 1))  # белый
    title = "Сертификат о прохождении курса"
    title_lines = simpleSplit(title, font_name, 28, width - 100)
    y = height - 30
    for line in title_lines:
        p.drawCentredString(width / 2, y, line)
        y -= 35

    # === ОСНОВНОЙ КОНТЕНТ (на белом фоне) ===
    content_top = height - 120
    content_bottom = 150
    content_width = width - 120

    # Белая карточка
    p.setFillColor(Color(1, 1, 1))
    p.roundRect(60, content_bottom, width - 120, content_top - content_bottom, 10, stroke=0, fill=1)

    # Текст внутри карточки
    p.setFillColor(text_color)
    y = content_top - 40

    p.setFont(font_name, 14)
    p.drawCentredString(width / 2, y, "Настоящим подтверждается, что")
    y -= 50

    # Имя пользователя
    user_name = completion.user.get_full_name() or completion.user.email
    p.setFont(font_name, 22)
    name_lines = simpleSplit(user_name, font_name, 22, content_width - 40)
    for line in name_lines:
        p.drawCentredString(width / 2, y, line)
        y -= 35

    y -= 20
    p.setFont(font_name, 14)
    p.drawCentredString(width / 2, y, "успешно завершил(а) курс")
    y -= 50

    # Название курса
    course_title = f"«{completion.course.title}»"
    p.setFont(font_name, 20)
    course_lines = simpleSplit(course_title, font_name, 20, content_width - 40)
    for line in course_lines:
        p.drawCentredString(width / 2, y, line)
        y -= 32

    y -= 40
    p.setFont(font_name, 12)
    p.setFillColor(Color(0.4, 0.4, 0.4))
    p.drawCentredString(width / 2, y, f"Дата выдачи: {completion.completed_at.strftime('%d.%m.%Y')}")
    y -= 20
    p.drawCentredString(width / 2, y, f"ID сертификата: {completion.certificate_id}")

    # Подпись
    y = 180
    p.setFillColor(text_color)
    p.setFont(font_name, 14)
    p.drawCentredString(width / 2, y, "Директор Центра финансовой грамотности Удмуртии")

    # === ДЕКОРАТИВНЫЙ ЭЛЕМЕНТ (линия или логотип внизу) ===
    p.setFillColor(primary_color)
    p.rect(0, 0, width, 30, stroke=0, fill=1)
    p.setFillColor(Color(1, 1, 1))
    p.setFont(font_name, 10)
    p.drawCentredString(width / 2, 10, "fingramota.udmurt.ru")

    # Сохранение
    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate_{course_id}.pdf"'
    return response