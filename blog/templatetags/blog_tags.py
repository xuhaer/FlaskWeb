from django import template
from django.db.models.aggregates import Count

from ..models import Article, Category, Tag

register = template.Library()


@register.simple_tag
def get_recent_articles(num=5):
    return Article.objects.all().order_by('-created_at')[:num]


@register.simple_tag
def archives():
    return Article.objects.dates('created_at', 'month', order='DESC')


@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)
    #return Category.objects.all()


@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)
