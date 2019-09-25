import markdown

from django.db.models import Q
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

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc'
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
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


class PostSearchView(View):

    def get(self, request):
        q = request.GET.get('q')
        if not q:
            msg = '请输入关键词'
        else:
            post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
        return render(request, 'post/index.html', locals())
