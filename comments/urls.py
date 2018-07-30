from django.urls import path

from . import views

app_name = 'comments'
urlpatterns = [
    path(r'comment/article/<int:article_pk>/', views.article_comment, name='article_comment'),
]
