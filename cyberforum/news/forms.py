from django import forms

from news.models import News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "content", "image", "is_published"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
