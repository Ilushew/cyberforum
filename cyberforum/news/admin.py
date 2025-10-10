from django.contrib import admin
from core.models import User
from news.models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_at", "is_published"]
    list_filter = ["is_published", "created_at", "author"]
    search_fields = ["title", "content"]
    date_hierarchy = "created_at"
    fields = ["title", "content", "author", "is_published", "image"]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["author"].queryset = User.objects.filter(is_moderator=True)
        return form