__author__ = "Frank Shen"

from django.urls import path

from .views import IndexView, TagView, ArchivesView, \
    CategoryView, PostDetailView, PostSearchView, IncreaseLikesView

app_name = 'post'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('post/<int:year>/<int:month>/', ArchivesView.as_view(), name='archives'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category'),
    path('tag/<int:pk>/', TagView.as_view(), name='tag'),
    path('search/', PostSearchView.as_view(), name='search'),
    path('likes/', IncreaseLikesView.as_view(), name='likes'),
]