import core.models

from django import forms


class LessonForm(forms.ModelForm):
    class Meta:
        model = core.models.Lesson
        fields = ['title', 'content', 'video_file', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'video_file': forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
