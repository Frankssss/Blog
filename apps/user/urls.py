__author__ = 'Frank Shen'

from django.urls import path

from .views import login, register, logout


app_name = 'accounts'
urlpatterns = [
    path('accounts/signin/', login, name='login'),
    path('accounts/signup/', register, name='register'),
    path('accoutns/signout/', logout, name='logout'),
]