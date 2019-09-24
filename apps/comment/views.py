from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from post.models import Post
from .models import Comment
from .forms import CommentForm


class PostComment(View):

    def post(self, request):
        data = {}
        form = CommentForm(request.POST, user=request.user)
        if form.is_valid():
            new_comment = Comment()
            new_comment.target = form.cleaned_data['post']
            new_comment.user = form.cleaned_data['user']
            new_comment.content = form.cleaned_data['content']
            parent = form.cleaned_data['parent']
            if parent is not None:
                new_comment.parent = parent
                new_comment.root = parent.root if parent.root is not None else parent
                new_comment.reply_to = parent.user
            new_comment.save()
            data.update({
                'status': 'SUCCESS',
                'comment_id': new_comment.id,
                'username': new_comment.user.username,
                'content': new_comment.content,
                'c_time': new_comment.c_time,
            })
            if parent is not None:
                data['root_id'] = new_comment.root.id
                data['reply_to'] = new_comment.reply_to.username
            else:
                data['reply_to'] = ''
        else:
            data.update({
                'status': 'ERROR',
                'msg': list(form.errors.values())[0]
            })
        return JsonResponse(data)
