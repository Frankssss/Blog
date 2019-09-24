__author__ = 'Frank Shen'

from django.urls import path

from .views import LoginView, RegisterView, LogoutView, UserConfirmView


app_name = 'user'
urlpatterns = [
    path('signin/', LoginView.as_view(), name='login'),
    path('signup/', RegisterView.as_view(), name='register'),
    path('signout/', LogoutView.as_view(), name='logout'),
    path('confirm/', UserConfirmView.as_view(), name='confirm')
]