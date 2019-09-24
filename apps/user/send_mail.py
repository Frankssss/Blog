__author__ = "Frank Shen"

import hashlib

from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from .models import ConfirmCode


def hash_code(s, salt='MySite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_code(user):
    code = hash_code(user.email)
    ConfirmCode.objects.create(code=code, user=user)
    return code


def send_ack_mail(mailto, code):
    title = '博客注册确认'
    text_content = '''感谢注册， 这里是Frank的博客网站，专注于技术记录与分享！\
        如果你看到这条消息，说明你的邮箱服务器不提供HTML连接功能， 请联系站长！
    '''
    url = '127.0.0.1:8000'
    html_content = f'''
        <p>感谢注册<a href="http://{url}/accounts/confirm/?code={code}" target=blank>Frank's Blog</a>，\
        专注于Python和Django技术的分享！</p>
        <p>请点击站点链接完成注册确认！</p>
        <p>此链接有效期为{settings.CONFIRM_DAYS}天！</p>
    '''
    msg = EmailMultiAlternatives(title, text_content, settings.EMAIL_HOST_USER, [mailto])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()