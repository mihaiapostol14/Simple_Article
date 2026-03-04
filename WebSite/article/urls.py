from django.urls import path
from . import views

app_name = 'article'   # 👈 THIS IS THE NAMESPACE

urlpatterns = [
    path('create-article/', views.CreateArticleView.as_view(), name='create-article'),
    path('article-list/', views.ArticleListView.as_view(), name='article-list'),
    path('article-detail/<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('update-article/<int:pk>/', views.UpdateArticleView.as_view(), name='update-article'),
    path('delete-article/<int:pk>/', views.DeleteArticleView.as_view(), name='delete-article'),
]