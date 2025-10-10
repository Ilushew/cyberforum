from django.shortcuts import render

from documentation.models import DocumentationFile


def documentation_view(request):
    docs = DocumentationFile.objects.all()
    return render(request, "documentations/documentation.html", {"docs": docs})
