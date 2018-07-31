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
    paginate_by = 1

    def get_context_data(self, **kwargs): 
        # 覆写 get_context_data 的目的是因为除了将 article 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、article 下的评论列表传递给模板。
        context = super().get_context_data(**kwargs)
        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        print('paginator, page, is_paginatedpaginator, page, is_paginated',paginator, page, is_paginated)
        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}

        left = []
        right = []
        left_has_more = False 
        right_has_more = False
        first = False
        last = False
        page_number = page.number # 用户请求的是第几页
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            print('fail')

            # 比如page_range是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            right = page_range[page_number:page_number + 2]
            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 比如page_range是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data

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
