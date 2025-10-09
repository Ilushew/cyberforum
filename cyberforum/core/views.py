import json
from datetime import datetime

from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt

from .forms import UserRegistrationForm, UserProfileForm
from .llm_assistant.rag import generate_answer
from .models import Contact, Event, AUDIENCE_CHOICES
from courses.models import Course
from courses.models import TestResult
from django.http import JsonResponse
from .models import Event
from courses.models import CourseCompletion

User = get_user_model()


def is_moderator(user):
    return user.is_authenticated and user.is_moderator


def home_view(request):
    courses = Course.objects.all()[:6]
    upcoming_events = Event.objects.order_by('date')[:3]
    contacts = Contact.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
    return render(request, 'core/home.html', {
        'courses': courses,
        'events': upcoming_events,
        'contacts': contacts,
    })


def contacts_view(request):
    contacts = Contact.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
    return render(request, 'core/contacts.html', {'contacts': contacts})


def textbooks_view(request):
    return render(request, 'core/textbooks.html')


def faq_view(request):
    faq_items = [
        {
            "question": "Что такое финансовая грамотность?",
            "answer": "Финансовая грамотность — это способность человека эффективно управлять своими финансами: планировать бюджет, сберегать, инвестировать, выбирать финансовые продукты и защищаться от мошенников."
        },
        {
            "question": "Кто может воспользоваться материалами портала?",
            "answer": "Наши материалы предназначены для всех: школьников, студентов, работающих граждан, пенсионеров и представителей малого бизнеса."
        },
        {
            "question": "Нужно ли платить за курсы?",
            "answer": "Нет, все материалы и курсы на портале предоставляются бесплатно в рамках государственной программы повышения финансовой грамотности."
        },
        {
            "question": "Как задать свой вопрос?",
            "answer": "Вы можете воспользоваться встроенным чат-ботом в правом нижнем углу сайта или связаться с нами через раздел «Контакты»."
        },
        {
            "question": "Где проходят очные мероприятия?",
            "answer": "Мы проводим встречи в школах, библиотеках, центрах социальной поддержки и других учреждениях Удмуртии. Актуальные события смотрите в разделе «События»."
        },
    ]
    return render(request, 'core/faq.html', {'faq_items': faq_items})


def events_view(request):
    events = Event.objects.all()

    # Получаем параметры из GET-запроса
    audience = request.GET.get('audience')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    # Фильтр по аудитории
    if audience and audience != '':
        events = events.filter(audience=audience)

    # Фильтр по дате "с"
    if date_from:
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            events = events.filter(date__gte=date_from)
        except ValueError:
            pass  # Игнорируем некорректные даты

    # Фильтр по дате "по"
    if date_to:
        try:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            events = events.filter(date__lte=date_to)
        except ValueError:
            pass

    # Сортируем по дате
    events = events.order_by('date')

    # Передаём в шаблон
    return render(request, 'core/events.html', {
        'events': events,
        'audience_choices': AUDIENCE_CHOICES,
        'current_filters': {
            'audience': audience or '',
            'date_from': date_from or '',
            'date_to': date_to or '',
        }
    })


@csrf_exempt
def chat_ask(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод не поддерживается'}, status=405)

    try:
        data = json.loads(request.body)
        question = data.get('question', '').strip()

        if not question:
            return JsonResponse({'error': 'Вопрос не может быть пустым'}, status=400)

        answer = generate_answer(question)

        return JsonResponse({'answer': answer})

    except Exception as e:
        return JsonResponse({'error': f'Ошибка сервера: {str(e)}'}, status=500)


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация прошла успешно! Проверьте email для подтверждения.")
            return redirect('core:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if not user.is_active:
                messages.error(request, "Пожалуйста, подтвердите ваш email, чтобы войти.")
            else:
                login(request, user)
                messages.success(request, f"Добро пожаловать, {user.email}!")
                return redirect('core:profile')
        else:
            messages.error(request, "Неверный email или пароль.")
    return render(request, 'core/login.html')


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
    return redirect('core:login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные обновлены!")
            return redirect('core:profile')
    else:
        form = UserProfileForm(instance=request.user)

    # Статистика
    test_results = TestResult.objects.filter(user=request.user)
    total_tests = test_results.count()
    avg_percent = test_results.aggregate(Avg('percent'))['percent__avg']
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
    return redirect('core:home')


def events_api_view(request):
    events = Event.objects.all()
    event_list = []
    for event in events:
        event_list.append({
            'title': event.title,
            'start': event.date.isoformat(),
            'extendedProps': {
                'description': event.description,
                'location': event.location,
                'audience': event.audience,
            },
            # Добавляем CSS-класс или data-атрибут через eventClassNames
            'eventClassNames': [f'audience-{event.audience}'],
        })
    return JsonResponse(event_list, safe=False)


def calendar_view(request):
    return render(request, 'core/calendar.html')


def news_list_view(request):
    news_list = News.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'core/news_list.html', {'news_list': news_list})


def news_detail_view(request, news_id):
    news_item = get_object_or_404(News, id=news_id, is_published=True)
    return render(request, 'core/news_detail.html', {'news': news_item})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import NewsForm
from .models import News


@user_passes_test(is_moderator, login_url='/login/')
def news_moderator_list(request):
    news_items = News.objects.all().order_by('-created_at')
    return render(request, 'core/news_moderator_list.html', {'news_list': news_items})


@user_passes_test(is_moderator, login_url='/login/')
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)  # ← request.FILES
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, "Новость успешно создана!")
            return redirect('core:news_moderator_list')
    else:
        form = NewsForm()
    return render(request, 'core/news_form.html', {'form': form, 'title': 'Создать новость'})


@user_passes_test(is_moderator, login_url='/login/')
def news_edit(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)  # ← request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, "Новость успешно обновлена!")
            return redirect('core:news_moderator_list')
    else:
        form = NewsForm(instance=news)
    return render(request, 'core/news_form.html', {'form': form, 'title': 'Редактировать новость'})


@user_passes_test(is_moderator, login_url='/login/')
def news_delete(request, news_id):
    """Удаление новости"""
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        news.delete()
        messages.success(request, "Новость удалена.")
        return redirect('core:news_moderator_list')
    return render(request, 'core/news_confirm_delete.html', {'news': news})


def event_detail_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'core/event_detail.html', {'event': event})
