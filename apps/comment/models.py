from django.db import models

from user.models import MyUser
from post.models import Post


class Comment(models.Model):
    user = models.ForeignKey(
        MyUser,
        related_name='user_comments',
        on_delete=models.CASCADE,
        verbose_name='评论人'
    )
    content = models.TextField()
    target = models.ForeignKey(
        Post,
        related_name='target',
        on_delete=models.CASCADE,
        verbose_name='目标'
    )
    reply_to = models.ForeignKey(
        MyUser,
        related_name='replies',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='回复给'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='父评论'
    )
    root = models.ForeignKey(
        'self',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='根评论'
    )
    c_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.content}'

    class Meta:
        db_table = 'comments'
        ordering = ['c_time']
        verbose_name = '评论'
        verbose_name_plural = verbose_name