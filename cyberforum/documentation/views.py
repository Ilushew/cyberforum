import documentation.models

from django.shortcuts import render


def documentation_view(request):
    docs = documentation.models.DocumentationFile.objects.all()
    return render(request, "documentations/documentation.html", {"docs": docs})
