import core.models
import courses.models
import events.models

from django.shortcuts import render


def search_view(request):
    query = request.GET.get("q", "").strip()
    audience = request.GET.get("audience", "")
    format_type = request.GET.get("format", "")

    Courses = courses.models.Course.objects.all()
    contacts = core.models.Contact.objects.all()
    Events = events.models.Event.objects.all()

    if query:
        Courses = Courses.filter(title__icontains=query) | Courses.filter(
            description__icontains=query
        )
        contacts = contacts.filter(name__icontains=query) | contacts.filter(
            address__icontains=query
        )
        Events = Events.filter(title__icontains=query) | Events.filter(
            description__icontains=query
        )

    if audience:
        Courses = Courses.filter(audience=audience)
        contacts = contacts.filter(audience=audience)
        Events = Events.filter(audience=audience)

    if format_type:
        Courses = Courses.filter(format_type=format_type)

    context = {
        "query": query,
        "courses": Courses,
        "contacts": contacts,
        "events": Events,
        "audience_filter": audience,
        "format_filter": format_type,
    }
    return render(request, "search/results.html", context)
