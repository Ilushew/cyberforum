import core.models
import news.models

from django.contrib import admin


@admin.register(news.models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_at", "is_published"]
    list_filter = ["is_published", "created_at", "author"]
    search_fields = ["title", "content"]
    date_hierarchy = "created_at"
    fields = ["title", "content", "author", "is_published", "image"]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["author"].queryset = core.models.User.objects.filter(is_moderator=True)
        return form

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change and obj.is_published:
            msg = (
                "📰 <b>Новая новость!</b>\n"
                f"<b>{obj.title}</b>\n"
                f"{obj.content[:200]}{'...' if len(obj.content) > 200 else ''}"
            )
            send_telegram_message(msg)
