import datetime
import events.models

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404


def events_view(request):
    Events = events.models.Event.objects.all()

    audience = request.GET.get("audience")
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")

    if audience and audience != "":
        Events = Events.filter(audience=audience)

    if date_from:
        try:
            date_from = datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
            Events = Events.filter(date__gte=date_from)
        except ValueError:
            pass

    if date_to:
        try:
            date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d").date()
            Events = Events.filter(date__lte=date_to)
        except ValueError:
            pass

    Events = Events.order_by("date")

    return render(
        request,
        "events/list.html",
        {
            "events": Events,
            "audience_choices": events.models.AUDIENCE_CHOICES,
            "current_filters": {
                "audience": audience or "",
                "date_from": date_from or "",
                "date_to": date_to or "",
            },
        },
    )


def get_audience_color(audience):
    colors = {
        "школьник": "#4285f4",   # Синий
        "пенсионер": "#34a853",  # Зелёный
        "МСП": "#fbbc04",        # Жёлтый
        "все": "#ea4335",        # Красный
    }
    return colors.get(audience, "#6a7d5d")


def events_api_view(request):
    Events = events.models.Event.objects.all()
    event_list = []
    for event in Events:
        event_list.append(
            {
                "title": event.title,
                "start": event.date.isoformat(),
                "audience": event.audience,
                "backgroundColor": get_audience_color(event.audience),
                "borderColor": get_audience_color(event.audience),             
                "extendedProps": {
                    "description": event.description,
                    "location": event.location,
                    "audience": event.audience,
                },
            }
        )
    return JsonResponse(event_list, safe=False)


def event_detail_view(request, event_id):
    event = get_object_or_404(events.models.Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})


def calendar_view(request):
    return render(request, "events/calendar.html")
