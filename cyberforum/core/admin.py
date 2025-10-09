from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Contact, User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительно", {"fields": ("phone", "is_moderator")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Дополнительно", {"fields": ("phone", "is_moderator")}),
    )
    list_display = UserAdmin.list_display + ("phone", "is_moderator")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "email", "audience"]
    search_fields = ["name", "address"]
    list_filter = ["audience"]
    fields = ["name", "address", "latitude", "longitude", "phone", "email", "audience"]