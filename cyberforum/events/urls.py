import events.views

from django.urls import path


app_name = "events"
urlpatterns = [
    path("", events.views.events_view, name="list"),
    path("<int:event_id>/", events.views.event_detail_view, name="detail"),
    path("api/events/", events.views.events_api_view, name="events_api"),
    path("calendar/", events.views.calendar_view, name="calendar"),
]
