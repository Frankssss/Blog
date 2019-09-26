import markdown

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
from mdeditor.fields import MDTextField

from user.models import MyUser


class Category(models.Model):
    name = models.CharField(verbose_name='名称', max_length=20)
    is_nav = models.BooleanField(verbose_name='是否是导航栏', default=False)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'
        verbose_name = '分类'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    name = models.CharField(verbose_name='名称', max_length=20)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tags'
        verbose_name = '标签云'
        verbose_name_plural = verbose_name


class Post(models.Model):
    title = models.CharField(verbose_name='标题', max_length=32)
    body = MDTextField(verbose_name='正文')
    views = models.PositiveIntegerField(verbose_name='浏览量', default=0)
    likes = models.PositiveIntegerField(verbose_name='点赞量', default=0)
    pub_time = models.DateTimeField(verbose_name='发布时间', auto_now_add=True)
    mod_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    category = models.ForeignKey(Category, verbose_name='文章分类', null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ForeignKey(Tag, verbose_name='文章标签', null=True, blank=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(MyUser, verbose_name='文章作者', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'posts'
        ordering = ['-pub_time']
        verbose_name = '文章'
        verbose_name_plural = verbose_name


@receiver(pre_save, sender=Post)
def delete_detail_cache(sender, instance=None, **kwargs):
    key = f'detail:{instance.id}'
    cache.delete(key)
    print('delete ', key)


@receiver(post_save, sender=Post)
def reset_detail_cache(sender, instance=None, **kwargs):
    key = f'detail:{instance.id}'
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc'
    ])
    instance.body = md.convert(instance.body)
    instance.toc = md.toc
    cache.set(key, instance, 5 * 60)
    print('reset ', key)
