from django.contrib import messages
from django.contrib.auth import get_user_model

from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, UpdateView

from .forms import ArticleForm
from .models import Article
from .utils import ArticleMixin


# Create your views here.

User = get_user_model()


class ArticleFormView(ArticleMixin, FormView):
    form_class = ArticleForm
    template_name = 'article/article.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['author'] = self.request.user
        return initial

    def form_valid(self, form):
        form.save()
        return super(ArticleFormView, self).form_valid(form=form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title=f'Create Article ({self.request.user})')

    def get_success_url(self):
        messages.success(request=self.request, message=f'create Article of {self.request.user} Successful')
        return reverse_lazy('home')


class ArticleListView(ArticleMixin, ListView):
    model = Article
    template_name = 'article/article_list.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title=f'Article List ({self.request.user})')


class ArticleUpdateView(ArticleMixin, UpdateView):
    form_class = ArticleForm
    model = Article
    template_name = 'article/article_update.html'