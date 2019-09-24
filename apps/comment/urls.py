__author__ = "Frank Shen"

from django.urls import path

from .views import PostComment

app_name = 'comment'
urlpatterns = [
    path('post-comment/', PostComment.as_view(), name='post-comment'),
]