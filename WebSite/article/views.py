from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)

from .forms import CreateArticleForm
from .models import Article
from .utils import ArticleMixin


class CreateArticleView(LoginRequiredMixin, ArticleMixin, CreateView):
    model = Article
    form_class = CreateArticleForm
    template_name = 'article/create_article.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['author'] = self.request.user.pk
        return initial

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Article created successfully!")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('article:article-list' ) # kwargs={'pk': self.request.user.pk}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title='Create Article')


class ArticleListView(ArticleMixin, ListView):
    model = Article
    template_name = 'article/article_list.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title='Article List')


class ArticleDetailView(ArticleMixin, DetailView):
    model = Article
    template_name = 'article/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title='Article Detail')


class UpdateArticleView(LoginRequiredMixin, ArticleMixin, UpdateView):
    model = Article
    form_class = CreateArticleForm
    template_name = 'article/update_article.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['author'] = self.request.user.pk
        return initial

    def form_valid(self, form):
        messages.success(self.request, "Article updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('article:article-list') # kwargs={'pk': self.object.pk}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title='Update Article')


class DeleteArticleView(LoginRequiredMixin, ArticleMixin, DeleteView):
    model = Article
    template_name = 'article/delete_article.html'
    success_url = reverse_lazy('article:article-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Article deleted successfully!")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title='Delete Article')