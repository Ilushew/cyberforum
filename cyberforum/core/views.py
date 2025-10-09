import json


from django.db.models import Avg
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegistrationForm, UserProfileForm
from .llm_assistant.rag import generate_answer
from .models import Contact
from courses.models import Course
from courses.models import TestResult
from django.http import JsonResponse
from django.shortcuts import redirect, render
from events.models import Event
from courses.models import CourseCompletion

User = get_user_model()


def is_moderator(user):
    return user.is_authenticated and user.is_moderator


def home_view(request):
    courses = Course.objects.all()[:6]
    upcoming_events = Event.objects.order_by("date")[:3]
    contacts = Contact.objects.exclude(latitude__isnull=True).exclude(
        longitude__isnull=True
    )
    return render(
        request,
        "core/home.html",
        {
            "courses": courses,
            "events": upcoming_events,
            "contacts": contacts,
        },
    )


def contacts_view(request):
    contacts = Contact.objects.exclude(latitude__isnull=True).exclude(
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
            "answer": "Вы можете воспользоваться встроенным чат-ботом в правом нижнем углу сайта или связаться с нами через раздел «Контакты»."
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
        return JsonResponse({"error": "Метод не поддерживается"}, status=405)

    try:
        data = json.loads(request.body)
        question = data.get("question", "").strip()

        if not question:
            return JsonResponse({"error": "Вопрос не может быть пустым"}, status=400)

        answer = generate_answer(question)

        return JsonResponse({"answer": answer})

    except Exception as e:
        return JsonResponse({"error": f"Ошибка сервера: {str(e)}"}, status=500)


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Регистрация прошла успешно! Проверьте email для подтверждения.",
            )
            return redirect("core:login")
    else:
        form = UserRegistrationForm()
    return render(request, "core/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if not user.is_active:
                messages.error(
                    request, "Пожалуйста, подтвердите ваш email, чтобы войти."
                )
            else:
                login(request, user)
                messages.success(request, f"Добро пожаловать, {user.email}!")
                return redirect("core:profile")
        else:
            messages.error(request, "Неверный email или пароль.")
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
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные обновлены!")
            return redirect("core:profile")
    else:
        form = UserProfileForm(instance=request.user)

    # Статистика
    test_results = TestResult.objects.filter(user=request.user)
    total_tests = test_results.count()
    avg_percent = test_results.aggregate(Avg("percent"))["percent__avg"]
    avg_percent = round(avg_percent, 1) if avg_percent is not None else 0

    # Пройденные курсы
    completed_courses = CourseCompletion.objects.filter(user=request.user).select_related('course')
    completed_courses_count = completed_courses.count()

    return render(request, 'core/profile.html', {
        'form': form,
        'total_tests': total_tests,
        'avg_percent': avg_percent,
        'completed_courses': completed_courses,
        'completed_courses_count': completed_courses_count,  # ← добавлено
    })


def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect("core:home")

from .telegram_utils import send_telegram_message

from .telegram_utils import send_telegram_message

from .telegram_utils import send_telegram_message

@user_passes_test(is_moderator, login_url='/login/')
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, "Событие успешно создано!")

            # === Отправка уведомления в Telegram ===
            msg = (
                f"📢 <b>Новое событие!</b>\n\n"
                f"<b>{event.title}</b>\n\n"
                f"📅 Дата: {event.date.strftime('%d.%m.%Y')}\n"
                f"📍 Место: {event.location}\n"
                f"👥 Аудитория: {event.get_audience_display()}\n\n"
                f"{event.description[:200]}{'...' if len(event.description) > 200 else ''}"
            )
            send_telegram_message(msg)

            return redirect('core:event_moderator_list')
    else:
        form = EventForm()
    return render(request, 'core/event_form.html', {'form': form, 'title': 'Создать событие'})


from .models import Textbook

def textbooks_view(request):
    textbooks = Textbook.objects.all()
    grouped = {}
    for code, name in Textbook.AUDIENCE_CHOICES:
        grouped[code] = textbooks.filter(audience=code)
    return render(request, 'core/textbooks.html', {
        'grouped_textbooks': grouped,
        'audiences': Textbook.AUDIENCE_CHOICES
    })


from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Textbook
from .forms import TextbookForm

def is_moderator(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_moderator, login_url='/login/')
def textbook_moderator_list(request):
    textbooks = Textbook.objects.all().order_by('-created_at')
    return render(request, 'core/textbook_moderator_list.html', {'textbooks': textbooks})

@user_passes_test(is_moderator, login_url='/login/')
def textbook_create(request):
    if request.method == 'POST':
        form = TextbookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Учебник успешно загружен!")
            return redirect('core:textbook_moderator_list')
    else:
        form = TextbookForm()
    return render(request, 'core/textbook_form.html', {'form': form, 'title': 'Загрузить учебник'})

@user_passes_test(is_moderator, login_url='/login/')
def textbook_delete(request, textbook_id):
    textbook = get_object_or_404(Textbook, id=textbook_id)
    if request.method == 'POST':
        textbook.delete()
        messages.success(request, "Учебник удалён.")
        return redirect('core:textbook_moderator_list')
    return render(request, 'core/textbook_confirm_delete.html', {'textbook': textbook})


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def telegram_webhook(request):
    try:
        data = json.loads(request.body)
        if 'message' in data:
            message = data['message']
            chat = message['chat']
            chat_id = chat['id']
            text = message.get('text', '')
            username = chat.get('username', '')

            if text == '/start':
                TelegramSubscriber.objects.update_or_create(
                    telegram_id=chat_id,
                    defaults={'username': username}
                )

        return JsonResponse({'ok': True})
    except Exception as e:
        print(f"Ошибка webhook: {e}")
        return JsonResponse({'error': str(e)}, status=500)


def event_detail_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'core/event_detail.html', {'event': event})


@user_passes_test(is_moderator, login_url='/login/')
def event_report_list(request):
    reports = EventReport.objects.all().order_by('-date')

    # Получаем параметры из GET
    title_query = request.GET.get('title', '').strip()
    audience = request.GET.get('audience', '')
    moderator_id = request.GET.get('moderator', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    # Фильтр по теме (поиск по частичному совпадению)
    if title_query:
        reports = reports.filter(title__icontains=title_query)

    # Фильтр по аудитории
    if audience:
        reports = reports.filter(audience=audience)

    # Фильтр по модератору
    if moderator_id and moderator_id.isdigit():
        reports = reports.filter(moderator_id=moderator_id)

    # Фильтр по дате "с"
    if date_from:
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            reports = reports.filter(date__gte=date_from)
        except ValueError:
            pass

    # Фильтр по дате "по"
    if date_to:
        try:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            reports = reports.filter(date__lte=date_to)
        except ValueError:
            pass

    # Получаем список модераторов для выпадающего списка
    moderators = User.objects.filter(is_moderator=True).only('id', 'email')

    context = {
        'reports': reports,
        'audience_choices': REPORT_AUDIENCE_CHOICES,
        'moderators': moderators,
        'current_filters': {
            'title': title_query,
            'audience': audience,
            'moderator': moderator_id,
            'date_from': date_from,
            'date_to': date_to,
        }
    }
    return render(request, 'core/event_report_list.html', context)

@user_passes_test(is_moderator, login_url='/login/')
def event_report_create(request):
    if request.method == 'POST':
        form = EventReportForm(request.POST)
        if form.is_valid():
            form.save(moderator=request.user)
            messages.success(request, "Отчёт успешно создан!")
            return redirect('core:event_report_list')
    else:
        form = EventReportForm()
    return render(request, 'core/event_report_form.html', {'form': form, 'title': 'Создать отчёт о мероприятии'})