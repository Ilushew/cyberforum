from django.contrib import admin
from events.models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "date", "location", "audience"]
    list_filter = ["audience", "date"]
    date_hierarchy = "date"