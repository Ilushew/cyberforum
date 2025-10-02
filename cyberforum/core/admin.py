from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Contact, Event, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Добавляем поле phone в админку
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('phone',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительно', {'fields': ('phone',)}),
    )
    list_display = UserAdmin.list_display + ('phone',)

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



