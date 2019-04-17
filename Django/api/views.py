from rest_framework import viewsets

from blog.models import Article
from comments.models import Comment
from .serializers import ArticleSerializer, CommentSerializer

class ArticleViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
