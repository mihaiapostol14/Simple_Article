from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from import_export import resources

# Register your models here.

User = get_user_model()

@admin.register(User)
class UserAdmin(UserAdmin):
    ...

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'photo']
        export_order = ('username', 'email', 'password', 'photo')