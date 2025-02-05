from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from .models import Article

User = get_user_model()


class ArticleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({
            'required': '',
            'type': 'text',
            'name': 'title',
            'id': 'title',
            'class': 'form-control',
            'placeholder': 'Article Title',
            'value': '',
            'maxlength': '50',
            'minlength': '5'
        }),

        self.fields['description'].widget.attrs.update({
            'required': '',
            'type': 'text',
            'name': 'description',
            'id': 'description',
            'class': 'form-control',
            'placeholder': 'Article Description',
            'value': '',
            'maxlength': '255',
            'minlength': '5'
        }),

        self.fields['pup_date'].widget.attrs.update({
            'required': '',
            'type': 'date',
            'name': 'pup_date',
            'id': 'pup_date',
            'class': 'form-control'
        }),

        self.fields['author'].widget.attrs.update({
            'required': '',
            'type': 'text',
            'name': 'author',
            'id': 'author',
            'class': 'form-control',
            'value': ''
        }),



    class Meta:
        model = Article
        fields = ['title', 'description', 'pup_date', 'author']
        # widgets = {
        #     'password': forms.PasswordInput(),
        # }


class ExportFormatForm(forms.Form):
    FORMAT_CHOICES = [
        ('csv', 'csv'),
        ('json', 'json'),
        ('pdf', 'pdf'),
    ]

    file_format = forms.ChoiceField(
        choices=FORMAT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
