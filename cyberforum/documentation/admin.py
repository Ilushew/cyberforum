from django.contrib import admin
from documentation.models import DocumentationFile

@admin.register(DocumentationFile)
class DocumentationFileAdmin(admin.ModelAdmin):
    list_display = ["title", "file", "uploaded_at"]
    list_per_page = 20
