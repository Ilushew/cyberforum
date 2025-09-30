import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .llm_assistant.rag import generate_answer
from .models import Contact, Event
from courses.models import Course



def home_view(request):
    courses = Course.objects.all()[:6]
    upcoming_events = Event.objects.order_by('date')[:3]
    return render(request, 'core/home.html', {
        'courses': courses,
        'events': upcoming_events,
    })


def contacts_view(request):
    contacts = Contact.objects.all()
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
