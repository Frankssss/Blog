from django.contrib import admin
from mdeditor.widgets import MDEditorWidget

from django.db import models
from .models import Post, Tag, Category


@admin.register(Post)
class Post(admin.ModelAdmin):
    list_display = ['title', 'author', 'pub_time', 'mod_time']
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget}
    }


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'c_time']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'c_time']

