import core.telegram_utils
import events.models

from django.contrib import admin


@admin.register(events.models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'audience']
    list_filter = ['audience', 'date']
    date_hierarchy = 'date'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:  # только при создании
            msg = (
                "📢 <b>Новое событие!</b>\n"
                f"<b>{obj.title}</b>\n"
                f"📅 Дата: {obj.date.strftime('%d.%m.%Y')}\n"
                f"📍 Место: {obj.location}\n"
                f"👥 Аудитория: {obj.get_audience_display()}\n"
                f"{obj.description[:200]}{'...' if len(obj.description) > 200 else ''}"
            )
            core.telegram_utils.send_telegram_message(msg)
