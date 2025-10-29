import documentation.models

from django import forms


class DocumentationFileForm(forms.ModelForm):
    class Meta:
        model = documentation.models.DocumentationFile
        fields = ["title", "file"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "file": forms.FileInput(attrs={"class": "form-control"}),
        }
