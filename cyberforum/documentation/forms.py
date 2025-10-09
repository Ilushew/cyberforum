from django import forms
from documentation.models import DocumentationFile


class DocumentationFileForm(forms.ModelForm):
    class Meta:
        model = DocumentationFile
        fields = ["title", "file"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "file": forms.FileInput(attrs={"class": "form-control"}),
        }
