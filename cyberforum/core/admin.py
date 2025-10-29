import core.models

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


@admin.register(core.models.User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительно", {"fields": ("phone", "is_moderator")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Дополнительно", {"fields": ("phone", "is_moderator")}),
    )
    list_display = UserAdmin.list_display + ("phone", "is_moderator")


@admin.register(core.models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "email", "audience"]
    search_fields = ["name", "address"]
    list_filter = ["audience"]
    fields = ["name", "address", "latitude", "longitude", "phone", "email", "audience"]


@admin.register(core.models.Textbook)
class TextbookAdmin(admin.ModelAdmin):
    list_display = ["title", "audience", "file"]
    list_filter = ["audience"]
    search_fields = ["title"]


