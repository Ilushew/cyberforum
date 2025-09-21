from django.shortcuts import render
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