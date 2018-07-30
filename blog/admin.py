from django.contrib import admin

# Register your models here.

from .models import Article, Category, Tag

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'modified_at', 'category', 'author']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)