import markdown

import datetime

from django.core.cache import cache
from django.db.models import Q, F
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView

from comment.forms import CommentForm
from comment.models import Comment
from .models import Post, Tag, Category


class IndexView(ListView):
    model = Post
    template_name = 'post/index.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'title': "Blog"
        })
        return context


class CategoryView(IndexView):
    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=category)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        context.update({
            'title': category.name
        })
        return context


class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        context.update({
            'title': tag.name
        })
        return context


class ArchivesView(IndexView):
    def get_queryset(self):
        return super(ArchivesView, self).get_queryset().filter(
            pub_time__year=self.kwargs.get('year'),
            pub_time__month=self.kwargs.get('month')
        )


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        key = f'detail:{pk}'
        post = cache.get(key)
        if not post:
            post = super(PostDetailView, self).get_object(queryset=None)
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc'
            ])
            post.body = md.convert(post.body)
            post.toc = md.toc
            cache.set(key, post, 60 * 5)
        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post = super(PostDetailView, self).get_object(queryset=None)
        form = CommentForm(initial={'target': post.id, 'parent': 0})
        post_list = Post.objects.filter(id__lt=post.id).order_by('-id')
        pre_post = post_list[0] if len(post_list) > 0 else None
        post_list = Post.objects.filter(id__gt=post.id).order_by('-id')
        next_post = post_list[0] if len(post_list) > 0 else None
        comment_list = Comment.objects.filter(target=post, parent=None)
        context.update({
            'form': form,
            'comment_list': comment_list,
            'pre_post': pre_post,
            'next_post': next_post,
        })
        return context

    def handle_visited(self):
        increase_pv = False
        uid = self.request.uid
        pv_key = f'pv:{uid}:{self.request.path}'

        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1*60*60)

        if increase_pv:
            Post.objects.filter(pk=self.object.id).update(views=F('views')+1)


class PostSearchView(IndexView):

    def get_queryset(self):
        queryset = super(PostSearchView, self).get_queryset()
        q = self.request.GET.get('q')
        if not q:
            return queryset
        else:
            return queryset.filter(Q(title__icontians=q) | Q(body__contains=q))


class IncreaseLikesView(View):

    def post(self, request):
        pk, data = self.request.POST.get('pk'), {}
        key = f'likes:{self.request.uid}:{self.request.path}'
        if not Post.objects.filter(pk=pk).exists():
            data.update({
                'msg': '文章不存在！',
                'status': 'ERROR'
            })
        elif key in cache:
            data.update({
                'msg': '已经点过攒了呀！',
                'status': 'ERROR',
            })
        else:
            Post.objects.filter(pk=pk).update(likes=F('likes')+1)
            cache.set(key, 60 * 60)
            data.update({
                'msg': '点赞成功！',
                'status': 'SUCCESS'
            })
        return JsonResponse(data)
