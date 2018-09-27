import random
import logging
import markdown

from markdown.extensions.toc import TocExtension
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from django_redis import get_redis_connection
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from comments.forms import CommentForm
from .models import Article


logger = logging.getLogger(__name__)
r = get_redis_connection("default")
# Create your views here.

# 修改文章后digest不会自动更改，可这样处理:
# for a in Article.objects.all():
#     a.save()

@method_decorator(cache_page(24 * 3600 + random.randint(0, 100)), name='dispatch')
class IndexView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    paginate_by = 5


@method_decorator(cache_page(24 * 3600 + random.randint(0, 100)), name='dispatch')
class ArticleDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        response = super(ArticleDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        article = super(ArticleDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        article.content = md.convert(article.content)
        return article

    def get_context_data(self, **kwargs): 
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


@method_decorator(cache_page(24 * 3600 + random.randint(0, 100)), name='dispatch')
class ArchivesView(ListView):
    model = Article
    template_name = 'blog/archive.html'
    context_object_name = 'article_list'
