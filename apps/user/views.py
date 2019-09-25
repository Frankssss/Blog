import datetime

from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import JsonResponse
from django.views import View

from .forms import MyUserCreationForm, MyAuthenticationForm
from .models import MyUser, ConfirmCode
from .send_mail import send_ack_mail, make_confirm_code


class LoginView(View):

    def get(self, request):
        title = '用户登录'
        form = MyAuthenticationForm()
        return render(request, 'user/login.html', locals())

    def post(self, request):
        data = {}
        form = MyAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = MyUser.objects.filter(Q(username=username) | Q(email=username)).first()
            login(request, user)
            data['status'] = 'SUCCESS'
        else:
            data.update({
                'status': 'ERROR',
                'msg': list(form.errors.values())[0][0]
            })
        return JsonResponse(data)


class RegisterView(View):

    def get(self, request):
        title = '用户注册'
        form = MyUserCreationForm()
        return render(request, 'user/register.html', locals())

    def post(self, request):
        data = {}
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email", '')
            user = MyUser.objects.filter(Q(email=email)).first()
            code = make_confirm_code(user)
            send_ack_mail(email, code)
            data.update({
                'status': 'SUCCESS',
                'msg': '注册成功， 请通过邮箱验证'
            })
        else:
            data.update({
                'status': 'ERROR',
                'msg': list(form.errors.values())[0][0]
            })
        return JsonResponse(data)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect(request.META['HTTP_REFERER'])


class UserConfirmView(View):

    def get(self, request):
        title = '注册确认'
        code = request.GET.get('code', '')
        msg = ''
        try:
            confirm = ConfirmCode.objects.get(code=code)
        except ObjectDoesNotExist:
            msg = '无效的确认请求'
        else:
            c_time = confirm.c_time
            now = datetime.datetime.now()
            if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
                confirm.user.delete()
                msg = '邮件确认码已过期， 请重新注册'
            else:
                confirm.user.has_confirmed = True
                confirm.user.save()
                confirm.delete()
                msg = '感谢确认邮件， 请前往登录！'
        return render(request, 'user/confirm.html', locals())

