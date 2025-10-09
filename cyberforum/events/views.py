from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from events.models import Event, AUDIENCE_CHOICES
from datetime import datetime


def events_view(request):
    events = Event.objects.all()

    audience = request.GET.get("audience")
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")

    if audience and audience != "":
        events = events.filter(audience=audience)

    if date_from:
        try:
            date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
            events = events.filter(date__gte=date_from)
        except ValueError:
            pass

    if date_to:
        try:
            date_to = datetime.strptime(date_to, "%Y-%m-%d").date()
            events = events.filter(date__lte=date_to)
        except ValueError:
            pass

    events = events.order_by("date")

    return render(
        request,
        "events/list.html",
        {
            "events": events,
            "audience_choices": AUDIENCE_CHOICES,
            "current_filters": {
                "audience": audience or "",
                "date_from": date_from or "",
                "date_to": date_to or "",
            },
        },
    )


def events_api_view(request):
    events = Event.objects.all()
    event_list = []
    for event in events:
        event_list.append(
            {
                "title": event.title,
                "start": event.date.isoformat(),
                "extendedProps": {
                    "description": event.description,
                    "location": event.location,
                    "audience": event.audience,
                },
                "eventClassNames": [f"audience-{event.audience}"],
            }
        )
    return JsonResponse(event_list, safe=False)

def event_detail_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "events/event_detail.html", {"event": event})

def calendar_view(request):
    return render(request, "events/calendar.html")