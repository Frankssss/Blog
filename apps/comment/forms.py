__author__ = "Frank Shen"

from django import forms
from django.db.models import ObjectDoesNotExist

from post.models import Post
from .models import Comment


class CommentForm(forms.Form):
    target = forms.IntegerField(widget=forms.HiddenInput)
    parent = forms.CharField(widget=forms.HiddenInput)
    content = forms.CharField(widget=forms.TextInput(attrs=
        {'class': 'form-control'}
    ))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户未登录')
        target = self.cleaned_data['target']
        try:
            post = Post.objects.get(id=target)
            self.cleaned_data['post'] = post
        except ObjectDoesNotExist:
            raise forms.ValidationError('文章不存在')
        else:
            parent = self.cleaned_data['parent']
        try:
            parent = int(parent)
        except ValueError:
            raise forms.ValidationError('回复出错')
        else:
            if parent < 0:
                raise forms.ValidationError('回复出错')
            elif parent == 0:
                self.cleaned_data['parent'] = None
            elif Comment.objects.filter(pk=parent).exists():
                self.cleaned_data['parent'] = Comment.objects.get(pk=parent)
            else:
                raise forms.ValidationError('回复出错')
        return self.cleaned_data
