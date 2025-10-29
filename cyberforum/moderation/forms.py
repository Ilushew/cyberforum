import courses.models

from django import forms


class CourseForm(forms.ModelForm):
    class Meta:
        model = courses.models.Course
        fields = ['title', 'description', 'audience', 'format_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'audience': forms.Select(attrs={'class': 'form-select'}),
            'format_type': forms.Select(attrs={'class': 'form-select'}),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = courses.models.Lesson
        fields = ['title', 'content', 'video_file', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'video_file': forms.FileInput(attrs={"class": "form-control", "accept": "video/*"}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = courses.models.Question
        fields = ['text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'option_a': forms.TextInput(attrs={'class': 'form-control'}),
            'option_b': forms.TextInput(attrs={'class': 'form-control'}),
            'option_c': forms.TextInput(attrs={'class': 'form-control'}),
            'option_d': forms.TextInput(attrs={'class': 'form-control'}),
            'correct_answer': forms.Select(
                choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
                attrs={'class': 'form-select'}
            ),
        }


QuestionFormSet = forms.inlineformset_factory(
    courses.models.Lesson, courses.models.Question, form=QuestionForm,
    extra=1, can_delete=True,
    fields=('text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer')
)
