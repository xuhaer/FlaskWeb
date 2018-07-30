import markdown
from .models import Article, Category
from django.shortcuts import render, get_object_or_404
from comments.forms import CommentForm


# Create your views here.
def index(request):
    article_list = Article.objects.all().order_by('-created_at')
    return render(request, 'blog/index.html', context={'article_list': article_list})


def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.increase_views()
    article.body = markdown.markdown(article.content,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    comment_list = article.comment_set.all()

    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'article': article,
               'form': form,
               'comment_list': comment_list
               }
    return render(request, 'blog/detail.html', context=context)


def archives(request, year, month):
    article_list = Article.objects.filter(created_at__year=year, created_at__month=month).order_by('-created_at')
    return render(request, 'blog/index.html', context={'article_list': article_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    article_list = Article.objects.filter(category=cate).order_by('-created_at')
    return render(request, 'blog/index.html', context={'article_list': article_list})
