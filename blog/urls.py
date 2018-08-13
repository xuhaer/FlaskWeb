from django.urls import path

from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('archives/', views.ArchivesView.as_view(), name='archives'),
]
