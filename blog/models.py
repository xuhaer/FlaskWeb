import markdown

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags 

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __repr__(self):
        return 'Category:{}'.format(self.name)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __repr__(self):
        return 'Tag:{}'.format(self.name)


class Article(models.Model):
    class Meta:
        ordering = ['-created_at']
        
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
       if not self.digest:
           md = markdown.Markdown(extensions=[
               'markdown.extensions.extra',
               'markdown.extensions.codehilite',
           ])
           # 先将 Markdown 文本渲染成 HTML 文本
           # strip_tags 去掉 HTML 文本的全部 HTML 标签
           self.digest = strip_tags(md.convert(self.content))[:32]

       # 调用父类的 save 方法将数据保存到数据库中
       super(Article, self).save(*args, **kwargs)
       
    title = models.CharField(max_length=64)
    content = models.TextField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField(auto_now=True)
    # 但默认情况下 CharField 要求我们必须存入数据,否则就会报错。
    # 指定 blank=True 后就可以允许空值了。
    digest = models.CharField(max_length=200, blank=True,help_text="可选项，若为空则摘要取正文前32个字符")
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    is_top = models.BooleanField(default=False)

    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True) #可以无标签
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    def __repr__(self):
        return 'Article:{}'.format(self.title)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
