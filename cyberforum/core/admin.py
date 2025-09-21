from django.contrib import admin
from .models import Contact, Event

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'audience']
    search_fields = ['name', 'address']
    list_filter = ['audience']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'audience']
    list_filter = ['audience', 'date']
    date_hierarchy = 'date'