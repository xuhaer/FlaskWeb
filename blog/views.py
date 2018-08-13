import markdown
from markdown.extensions.toc import TocExtension
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from django.db.models import Q

from .models import Article, Category#, Tag
from comments.forms import CommentForm


# Create your views here.

# 修改文章后digest不会自动更改，可这样处理:
# for a in Article.objects.all():
#     a.save()

class IndexView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    paginate_by = 5
  
            
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


class ArchivesView(ListView):
    model = Article
    template_name = 'blog/archive.html'
    context_object_name = 'article_list'
