from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    DetailView,
    UpdateView,
    FormView
)
from easy_pdf.views import PDFTemplateResponseMixin

from .admin import UserResource
from .forms import (
    RegistrationUserForm,
    ChangeUserPasswordForm,
    LoginUserForm,
    ExportFormatForm,
    UpdateUserForm
)
from .utils import AuthorizationUserMixin

User = get_user_model()


class RegistrationUserView(View):
    template_name = 'authentication_user/registration_user.html'

    def get(self, request):
        context = {
            'title': 'Registration',
            'form': RegistrationUserForm()
        }
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request):
        form = RegistrationUserForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()

            login(request=request, user=user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request=self.request, message=f'Registration {request.user} Successful')
            return redirect('user-profile')
        context = {
            'form': form
        }
        return render(request=request, template_name=self.template_name, context=context)


class LoginUserView(AuthorizationUserMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'authentication_user/login_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title='Login User')

    def get_success_url(self):
        messages.success(request=self.request, message=f'Login {self.request.user} Successful')
        return reverse_lazy('home')


class PDFUserDetailView(PDFTemplateResponseMixin, DetailView):
    model = User
    template_name = 'authentication_user/pdf_user_profile.html'

    base_url = f"{'file://'}{settings.STATIC_ROOT}"

    def get_context_data(self, **kwargs):
        return super(PDFUserDetailView, self).get_context_data(
            pagesize='A4',
            **kwargs
        )


class UserDetailView(AuthorizationUserMixin, DetailView, FormView):  # TODO: UserDetailView
    model = User
    form_class = ExportFormatForm
    template_name = 'authentication_user/user_profile.html'
    context_object_name = 'user'

    def get_queryset(self):
        user_pk = self.request.user.pk
        return User.objects.filter(pk=user_pk)

    def post(self, request, *args, **kwargs):
        qs = self.get_queryset()
        dataset = UserResource().export(queryset=qs)

        file_format = self.request.POST.get('file_format')

        if file_format == 'csv':
            ds = dataset.csv
        else:
            ds = dataset.json

        response = HttpResponse(ds, content_type=f'{file_format}')
        response[
            'Content-Disposition'] = f'attachment; filename="Personal Information {self.request.user}.{file_format}"'
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title=f'Profile ({self.request.user})')


class UserUpdateView(AuthorizationUserMixin, UpdateView):  # TODO: UserUpdateView
    model = User
    form_class = UpdateUserForm
    template_name = 'authentication_user/update_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title=f'update {self.request.user}')


class ChangeUserPasswordView(AuthorizationUserMixin, PasswordChangeView):  # TODO: ChangeUserPasswordView
    template_name = 'authentication_user/change_password.html'
    form_class = ChangeUserPasswordForm

    def get_success_url(self):
        messages.success(request=self.request, message=f'Change Password {self.request.user} Successful')
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context)


def logout_view(request):
    logout(request=request)
    return redirect('home')
