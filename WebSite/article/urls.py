from django.urls import path
from . import views


urlpatterns = [
    path('create-article/', views.ArticleFormView.as_view(), name='create-article'),
    path('article-list/', views.ArticleListView.as_view(), name='article-list'),
    path('article-update/<int:pk>/', views.ArticleUpdateView.as_view(), name='article-update'),
    path('article-delete/<int:pk>/', views.ArticleDeleteView.as_view(), name='article-delete'),
]
