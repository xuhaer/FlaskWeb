import markdown
from .models import Article, Category
from comments.forms import CommentForm

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

# Create your views here.
# def index(request):
#     article_list = Article.objects.all().order_by('-created_at')
#     return render(request, 'blog/index.html', context={'article_list': article_list})

class IndexView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'


# def detail(request, pk):
#     article = get_object_or_404(Article, pk=pk)
#     article.increase_views()
#     article.content = markdown.markdown(article.content,
#                                   extensions=[
#                                       'markdown.extensions.extra',
#                                       'markdown.extensions.codehilite',
#                                       'markdown.extensions.toc',
#                                   ])
#     form = CommentForm()
#     comment_list = article.comment_set.all()

#     # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
#     context = {'article': article,
#                'form': form,
#                'comment_list': comment_list
#                }
#     return render(request, 'blog/detail.html', context=context)

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
        article.content = markdown.markdown(article.content,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
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


# def archives(request, year, month):
#     article_list = Article.objects.filter(created_at__year=year, created_at__month=month).order_by('-created_at')
#     return render(request, 'blog/index.html', context={'article_list': article_list})

class ArchivesView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_at__year=year,created_at__month=month)


# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     article_list = Article.objects.filter(category=cate).order_by('-created_at')
#     return render(request, 'blog/index.html', context={'article_list': article_list})

class CategoryView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=category)
