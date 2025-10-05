import json

from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt

from .forms import UserRegistrationForm, UserProfileForm
from .llm_assistant.rag import generate_answer
from .models import Contact, Event
from courses.models import Course
from courses.models import TestResult

User = get_user_model()


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


def events_view(request):
    events = Event.objects.order_by('date')
    return render(request, 'core/events.html', {'events': events})


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

    # Статистика пользователя
    test_results = TestResult.objects.filter(user=request.user)
    total_tests = test_results.count()
    avg_percent = test_results.aggregate(Avg('percent'))['percent__avg']
    avg_percent = round(avg_percent, 1) if avg_percent is not None else 0

    return render(request, 'core/profile.html', {
        'form': form,
        'total_tests': total_tests,
        'avg_percent': avg_percent,
    })

def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect('core:home')