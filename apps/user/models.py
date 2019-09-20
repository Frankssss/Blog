from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    has_confirmed = models.BooleanField(verbose_name='是否确认', default=False)
    mobile = models.CharField(verbose_name='手机号', max_length=20)
    nick_name = models.CharField(verbose_name='昵称', max_length=20)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class ConfirmCode(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    code = models.CharField(verbose_name='确认码', max_length=256)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.code}'

    class Meta:
        ordering = ['c_time']
        db_table = 'confirmCode'
        verbose_name = '确认码'
        verbose_name_plural = verbose_name
