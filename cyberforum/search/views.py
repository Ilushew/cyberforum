from django.shortcuts import render

from core.models import Contact
from courses.models import Course
from events.models import Event


def search_view(request):
    query = request.GET.get("q", "").strip()
    audience = request.GET.get("audience", "")
    format_type = request.GET.get("format", "")

    courses = Course.objects.all()
    contacts = Contact.objects.all()
    events = Event.objects.all()

    if query:
        courses = courses.filter(title__icontains=query) | courses.filter(
            description__icontains=query
        )
        contacts = contacts.filter(name__icontains=query) | contacts.filter(
            address__icontains=query
        )
        events = events.filter(title__icontains=query) | events.filter(
            description__icontains=query
        )

    if audience:
        courses = courses.filter(audience=audience)
        contacts = contacts.filter(audience=audience)
        events = events.filter(audience=audience)

    if format_type:
        courses = courses.filter(format_type=format_type)

    context = {
        "query": query,
        "courses": courses,
        "contacts": contacts,
        "events": events,
        "audience_filter": audience,
        "format_filter": format_type,
    }
    return render(request, "search/results.html", context)
