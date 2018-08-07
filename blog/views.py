import markdown
from markdown.extensions.toc import TocExtension
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from django.db.models import Q

from .models import Article, Category#, Tag
from comments.forms import CommentForm


# Create your views here.

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
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Article 模型实例，即被访问的文章 article
        response = super(ArticleDetailView, self).get(request, *args, **kwargs)
        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章article
        self.object.increase_views()
        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 article 的 content 值进行渲染
        article = super(ArticleDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        article.content = md.convert(article.content)
        article.toc = md.toc
        return article

    def get_context_data(self, **kwargs): 
        # 覆写 get_context_data 的目的是因为除了将 article 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、article 下的评论列表传递给模板。
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

    # def get_queryset(self):
    #     year = self.kwargs.get('year')
    #     month = self.kwargs.get('month')
    #     return super(ArchivesView, self).get_queryset().filter(created_at__year=year,created_at__month=month)

# def archives(request, year, month):
#     article_list = Article.objects.filter(created_at__year=year, created_at__month=month).order_by('-created_at')
#     return render(request, 'blog/index.html', context={'article_list': article_list})


# class CategoryView(ListView):
#     model = Article
#     template_name = 'blog/index.html'
#     context_object_name = 'article_list'

#     def get_queryset(self):
#         category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
#         return super(CategoryView, self).get_queryset().filter(category=category)


# class TagView(ListView):
#     model = Article
#     template_name = 'blog/index.html'
#     context_object_name = 'article_list'

#     def get_queryset(self):
#         tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
#         return super(TagView, self).get_queryset().filter(tags=tag)

# def archives(request, year, month):
#     article_list = Article.objects.filter(created_at__year=year, created_at__month=month).order_by('-created_at')
#     return render(request, 'blog/index.html', context={'article_list': article_list})


def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "请输入关键词"
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    article_list = Article.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'article_list': article_list})
