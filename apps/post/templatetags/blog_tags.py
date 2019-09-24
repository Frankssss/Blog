__author__ = "Frank Shen"

from django import template
from django.db.models.aggregates import Count

from ..models import Post, Tag, Category

register = template.Library()


@register.simple_tag
def get_host_posts(num=5):
    return Post.objects.all().order_by('-views')[:num]


@register.simple_tag
def archives():
    return Post.objects.dates('pub_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
