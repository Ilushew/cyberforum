import core.forms
import core.llm_assistant
import core.models
import courses.models
import datetime
import events.forms
import events.models
import openpyxl

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404


User = get_user_model()


def is_moderator(user):
    return user.is_authenticated and user.is_moderator


def home_view(request):
    Courses = courses.models.Course.objects.all()[:6]
    upcoming_events = events.models.Event.objects.order_by("date")[:3]
    contacts = core.models.Contact.objects.exclude(latitude__isnull=True).exclude(
        longitude__isnull=True
    )
    return render(
        request,
        "core/home.html",
        {
            "courses": Courses,
            "events": upcoming_events,
            "contacts": contacts,
        },
    )


def contacts_view(request):
    contacts = core.models.Contact.objects.exclude(latitude__isnull=True).exclude(
        longitude__isnull=True
    )
    return render(request, "core/contacts.html", {"contacts": contacts})


def textbooks_view(request):
    return render(request, "core/textbooks.html")


def faq_view(request):
    faq_items = [
        {
            "question": "Что такое финансовая грамотность?",
            "answer": "Финансовая грамотность — это способность человека эффективно управлять своими финансами: планировать бюджет, сберегать, инвестировать, выбирать финансовые продукты и защищаться от мошенников.",
        },
        {
            "question": "Кто может воспользоваться материалами портала?",
            "answer": "Наши материалы предназначены для всех: школьников, студентов, работающих граждан, пенсионеров и представителей малого бизнеса.",
        },
        {
            "question": "Нужно ли платить за курсы?",
            "answer": "Нет, все материалы и курсы на портале предоставляются бесплатно в рамках государственной программы повышения финансовой грамотности.",
        },
        {
            "question": "Как задать свой вопрос?",
            "answer": "Вы можете воспользоваться встроенным чат-ботом в правом нижнем углу сайта или связаться с нами через раздел «Контакты».",
        },
        {
            "question": "Где проходят очные мероприятия?",
            "answer": "Мы проводим встречи в школах, библиотеках, центрах социальной поддержки и других учреждениях Удмуртии. Актуальные события смотрите в разделе «События».",
        },
    ]
    return render(request, "core/faq.html", {"faq_items": faq_items})


@csrf_exempt
def chat_ask(request):
    if request.method != "POST":
        return HttpResponse({"error": "Метод не поддерживается"}, status=405)

    try:
        data = json.loads(request.body)
        question = data.get("question", "").strip()

        if not question:
            return HttpResponse({"error": "Вопрос не может быть пустым"}, status=400)

        answer = core.llm_assistant.rag.generate_answer(question)

        return HttpResponse({"answer": answer})

    except Exception as e:
        return HttpResponse({"error": f"Ошибка сервера: {str(e)}"}, status=500)


def register_view(request):
    if request.method == "POST":
        form = core.forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Регистрация прошла успешно! Проверьте вашу почту для подтверждения email.",
                extra_tags='registration_success'
            )
            return redirect("core:login")
    else:
        form = core.forms.UserRegistrationForm()
    return render(request, "core/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        storage = messages.get_messages(request)
        storage.used = True
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if not user.is_active:
                messages.error(request, "Пожалуйста, подтвердите ваш email, чтобы войти.")
            else:
                login(request, user)
                return redirect("core:profile")
        else:
            messages.error(request, "Неверный email или пароль. Возможно вы не подтвердили почту")
    return render(request, "core/login.html")


def confirm_email_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.email_verified = True
        user.save()
        messages.success(request, "Ваш email подтверждён! Теперь вы можете войти.")
    else:
        messages.error(request, "Ссылка недействительна или устарела.")
    return redirect("core:login")


@login_required
def profile_view(request):
    if request.method == "POST":
        form = core.forms.UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные обновлены!")
            return redirect("core:profile")
    else:
        form = core.forms.UserProfileForm(instance=request.user)

    # Статистика
    test_results = courses.models.TestResult.objects.filter(user=request.user)
    total_tests = test_results.count()
    avg_percent = test_results.aggregate(Avg("percent"))["percent__avg"]
    avg_percent = round(avg_percent, 1) if avg_percent is not None else 0

    # Пройденные курсы
    completed_courses = courses.models.CourseCompletion.objects.filter(
        user=request.user
    ).select_related("course")
    completed_courses_count = completed_courses.count()

    return render(
        request,
        "core/profile.html",
        {
            "form": form,
            "total_tests": total_tests,
            "avg_percent": avg_percent,
            "completed_courses": completed_courses,
            "completed_courses_count": completed_courses_count,  # ← добавлено
        },
    )


def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect("core:home")


def textbooks_view(request):
    textbooks = core.models.Textbook.objects.all()
    grouped = {}
    for code, name in core.models.Textbook.AUDIENCE_CHOICES:
        grouped[code] = textbooks.filter(audience=code)
    return render(
        request,
        "core/textbooks.html",
        {"grouped_textbooks": grouped, "audiences": core.models.Textbook.AUDIENCE_CHOICES},
    )


def is_moderator(user):
    return user.is_staff or user.is_superuser


@user_passes_test(is_moderator, login_url="/login/")
def textbook_moderator_list(request):
    textbooks = core.models.Textbook.objects.all().order_by("-created_at")
    return render(
        request, "core/textbook_moderator_list.html", {"textbooks": textbooks}
    )


@user_passes_test(is_moderator, login_url="/login/")
def textbook_create(request):
    if request.method == "POST":
        form = core.forms.TextbookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Учебник успешно загружен!")
            return redirect("core:textbook_moderator_list")
    else:
        form = core.forms.TextbookForm()
    return render(
        request, "core/textbook_form.html", {"form": form, "title": "Загрузить учебник"}
    )


@user_passes_test(is_moderator, login_url="/login/")
def textbook_delete(request, textbook_id):
    textbook = get_object_or_404(core.models.Textbook, id=textbook_id)
    if request.method == "POST":
        textbook.delete()
        messages.success(request, "Учебник удалён.")
        return redirect("core:textbook_moderator_list")
    return render(request, "core/textbook_confirm_delete.html", {"textbook": textbook})


def event_detail_view(request, event_id):
    event = get_object_or_404(events.models.Event, id=event_id)
    return render(request, "core/event_detail.html", {"event": event})


@user_passes_test(is_moderator, login_url="/login/")
def event_report_list(request):
    reports = core.models.EventReport.objects.all().order_by("-date")

    # Получаем параметры из GET
    title_query = request.GET.get("title", "").strip()
    audience = request.GET.get("audience", "")
    moderator_id = request.GET.get("moderator", "")
    date_from = request.GET.get("date_from", "")
    date_to = request.GET.get("date_to", "")

    # Фильтр по теме (поиск по частичному совпадению)
    if title_query:
        reports = reports.filter(title__icontains=title_query)

    # Фильтр по аудитории
    if audience:
        reports = reports.filter(audience=audience)

    # Фильтр по модератору
    if moderator_id and moderator_id.isdigit():
        reports = reports.filter(moderator_id=moderator_id)

    # Фильтр по дате
    if date_from:
        try:
            date_from = datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
            reports = reports.filter(date__gte=date_from)
        except ValueError:
            pass

    if date_to:
        try:
            date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d").date()
            reports = reports.filter(date__lte=date_to)
        except ValueError:
            pass

    # Получаем список модераторов для выпадающего списка
    moderators = User.objects.filter(is_moderator=True).only("id", "email")

    context = {
        "reports": reports,
        "audience_choices": core.models.REPORT_AUDIENCE_CHOICES,
        "moderators": moderators,
        "current_filters": {
            "title": title_query,
            "audience": audience,
            "moderator": moderator_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    }
    return render(request, "core/event_report_list.html", context)


@user_passes_test(is_moderator, login_url="/login/")
def event_report_create(request):
    if request.method == "POST":
        form = events.forms.EventReportForm(request.POST)
        if form.is_valid():
            form.save(moderator=request.user)
            messages.success(request, "Отчёт успешно создан!")
            return redirect("core:event_report_list")
    else:
        form = events.forms.EventReportForm()
    return render(
        request,
        "core/event_report_form.html",
        {"form": form, "title": "Создать отчёт о мероприятии"},
    )


def export_reports_to_excel(request):
    reports = core.models.EventReport.objects.select_related('moderator').all()

    title_query = request.GET.get('title', '').strip()
    audience = request.GET.get('audience', '')
    moderator_id = request.GET.get('moderator', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    if title_query:
        reports = reports.filter(title__icontains=title_query)

    if audience:
        reports = reports.filter(audience=audience)

    if moderator_id and moderator_id.isdigit():
        reports = reports.filter(moderator_id=int(moderator_id))

    if date_from:
        parsed_date = parse_date(date_from)
        if parsed_date:
            reports = reports.filter(date__gte=parsed_date)

    if date_to:
        parsed_date = parse_date(date_to)
        if parsed_date:
            reports = reports.filter(date__lte=parsed_date)

    reports = reports.order_by('date')

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Отчёты"

    columns = [
        'ID', 'Тема', 'Аудитория', 'Дата', 'Слушатели',
        'Комментарии', 'Модератор', 'Создано'
    ]
    worksheet.append(columns)

    for report in reports:
        worksheet.append([
            report.id,
            report.title,
            report.get_audience_display(),
            report.date.strftime('%d.%m.%Y') if report.date else '',
            report.listener_count or '',
            report.comments or '',
            report.moderator.email if report.moderator else '',
            report.created_at.strftime('%d.%m.%Y %H:%M') if report.created_at else '',
        ])

    for i, col in enumerate(columns, start=1):
        worksheet.column_dimensions[openpyxl.utils.get_column_letter(i)].width = len(col) + 2

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="filtered_reports.xlsx"'
    workbook.save(response)
    return response
