__author__ = 'Frank Shen'

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q


from .models import MyUser


class MyAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': '用户名或邮箱'
        })
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': '密码'
        })

    def clean(self):
        username = self.cleaned_data['username']
        user = MyUser.objects.filter(Q(username=username) | Q(email=username)).first()
        if not user:
            raise forms.ValidationError('该账号不存在，请检查输入是否正确')
        if not user.has_confirmed:
            raise forms.ValidationError('该账号尚未激活, 请先确认邮件')
        return super(MyAuthenticationForm, self).clean()


class MyUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': '密码'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': '重复密码'
        })

    def clean(self):
        email = self.cleaned_data['email']
        user = MyUser.objects.filter(email=email).first()
        if user and user.has_confirmed:
            raise forms.ValidationError('该邮箱已注册，请直接登录')
        return super(MyUserCreationForm, self).clean()

    class Meta:
        model = MyUser
        fields = UserCreationForm.Meta.fields + ('email',)
        widgets = {
            'email': forms.widgets.TextInput(attrs={
                'class': 'form-control', 'placeholder': '邮箱地址'
            }),
            'username': forms.widgets.TextInput(attrs={
                'class': 'form-control', 'placeholder': '用户名'
            })
        }
