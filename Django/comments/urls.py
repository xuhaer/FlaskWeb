from django.urls import path, include

from . import views

app_name = 'comments'
urlpatterns = [
    path('comment/article/<int:article_pk>/', views.article_comment, name='article_comment'),
    path('ajax_val/', views.ajax_val, name='ajax_val'), #ajax动态校验验证码的正确性
]
