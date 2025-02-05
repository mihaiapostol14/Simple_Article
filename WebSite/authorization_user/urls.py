from django.urls import path
from . import views


urlpatterns = [
    path('registration-user/', views.RegistrationUserView.as_view(), name='registration-user'),
    path('user-profile/<int:pk>/', views.UserDetailView.as_view(), name='user-profile'),
    path('pdf_file/<int:pk>/',views.PDFUserDetailView.as_view(), name='pdf_file'),
    path('update-user/<int:pk>/', views.UserUpdateView.as_view(), name='update-user'),
    path('login-user/', views.LoginUserView.as_view(), name='login-user'),
    path('change-password/', views.ChangeUserPasswordView.as_view(), name='change-password'),
    path('logout-user/', views.logout_view, name='logout-user'),

]
