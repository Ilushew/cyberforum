from django.urls import path

from events.views import event_detail_view, calendar_view
from . import views


app_name = "events"
urlpatterns = [
    path("", views.events_view, name="list"),
    path("<int:event_id>/", event_detail_view, name="detail"),
    path("api/events/", views.events_api_view, name="events_api"),
    path("calendar/", calendar_view, name="calendar"),
]
