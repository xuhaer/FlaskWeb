from django.urls import path

from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('archives/', views.ArchivesView.as_view(), name='archives'),
    # path('category/<int:pk>/', views.CategoryView.as_view(), name='category'),
    # path('tag/<int:pk>/', views.TagView.as_view(), name='tag'),
    # path('search/', views.search, name='search'),
    # path('contact/', views.contact, name='contact'),

]
