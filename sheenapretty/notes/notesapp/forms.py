from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Course, Note


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'note_date', 'course', 'pinned', 'content']
        widgets = {
            'note_date': forms.DateInput(attrs={'type': 'date'}),
            'content': forms.Textarea(attrs={'rows': 16}),
        }


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')
