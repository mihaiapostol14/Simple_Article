from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<int:year>/<str:month>', views.HomeView.as_view(), name='home'),

]
