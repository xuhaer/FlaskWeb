from django.contrib.syndication.views import Feed

from .models import Article


class ArticlesRssFeed(Feed):
    title = "MyBlog"
    link = "/"
    description = "MyBlog RSS FEED"

    # 需要显示的内容条目
    def items(self):
        return Article.objects.all()

    # 聚合器中显示的内容条目的标题
    def item_title(self, item):
        return '{}:{}'.format(item.category.name, item.title)

    # 聚合器中显示的内容条目的描述
    def item_description(self, item):
        return item.content
