from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.forms import ModelForm

User = get_user_model()


class RegistrationUserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'required': '',
            'type': 'text',
            'name': 'username',
            'id': 'username',
            'class': 'form-control',
            'placeholder': 'Peter',
            'value': '',
            'maxlength': '50',
            'minlength': '5'
        }),

        self.fields['email'].widget.attrs.update({
            'required': '',
            'type': 'email',
            'name': 'email',
            'id': 'email',
            'class': 'form-control',
            'placeholder': 'PiterParker@gmail.com',
            'value': ''
        })

        self.fields['password'].widget.attrs.update({
            'required': '',
            'type': 'password',
            'name': 'password',
            'id': 'password',
            'class': 'form-control',
            'placeholder': 'PiterParker1234',
            'value': '',
            'maxlength': '8',
            'minlength': '5'
        })

        self.fields['photo'].widget.attrs.update({
            'type': 'image',
            'name': 'photo',
            'id': 'photo',
            'class': 'form-control',
            'maxlength': '8',

        })

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'photo']
        widgets = {
            'password': forms.PasswordInput(),
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = User
        fields = ['username', 'password']


class ChangeUserPasswordForm(PasswordChangeForm):
    new_password1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    new_password2 =  forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']


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