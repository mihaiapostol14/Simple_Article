from django.urls import path
from . import views


urlpatterns = [
    path('create-article/', views.ArticleFormView.as_view(), name='create-article'),
]
