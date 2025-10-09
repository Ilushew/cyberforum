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
    list_display = ['name', 'phone', 'email', 'audience']
    search_fields = ['name', 'address']
    list_filter = ['audience']
    fields = ['name', 'address', 'latitude', 'longitude', 'phone', 'email', 'audience']


from .telegram_utils import send_telegram_message

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'audience']
    list_filter = ['audience', 'date']
    date_hierarchy = 'date'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:
            msg = (
                f"📢 <b>Новое событие!</b>\n\n"
                f"<b>{obj.title}</b>\n"
                f"📅 Дата: {obj.date.strftime('%d.%m.%Y')}\n"
                f"📍 Место: {obj.location}\n"
                f"👥 Аудитория: {obj.get_audience_display()}\n\n"
                f"{obj.description[:200]}{'...' if len(obj.description) > 200 else ''}"
            )
            send_telegram_message(msg)


from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'is_published']
    list_filter = ['is_published', 'created_at', 'author']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'
    fields = ['title', 'content', 'author', 'is_published', 'image']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Ограничиваем выбор автора только модераторами
        form.base_fields['author'].queryset = User.objects.filter(is_moderator=True)
        return form


from .models import DocumentationFile

@admin.register(DocumentationFile)
class DocumentationFileAdmin(admin.ModelAdmin):
    list_display = ['title', 'file', 'uploaded_at']
    list_per_page = 20


from .models import Textbook

@admin.register(Textbook)
class TextbookAdmin(admin.ModelAdmin):
    list_display = ['title', 'audience', 'file']
    list_filter = ['audience']
    search_fields = ['title']
