import documentation.models

from django.contrib import admin


@admin.register(documentation.models.DocumentationFile)
class DocumentationFileAdmin(admin.ModelAdmin):
    list_display = ["title", "file", "uploaded_at"]
    list_per_page = 20
