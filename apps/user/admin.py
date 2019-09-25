from django.contrib import admin

from .models import MyUser, ConfirmCode


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'has_confirmed']


@admin.register(ConfirmCode)
class ConfirmCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'c_time']