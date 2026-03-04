from django import forms
from django.contrib.auth import get_user_model

from .models import Article

User = get_user_model()


class CreateArticleForm(forms.ModelForm): # README: CreateArticleForm 👈
    title = forms.CharField(
        required=True,
        label="Title",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter article title...'
        })
    )

    description = forms.CharField(
        required=True,
        label="Description",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Write your content here...',
            'rows': '6'
        })
    )

    author = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        empty_label=None,
        required=False,
        label="Author",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    class Meta:
        model = Article
        fields = ['title', 'description', 'author']
