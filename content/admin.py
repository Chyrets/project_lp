from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Tag, Post, PostReaction, Comment


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Настройка отображения модели Tag в админке"""
    list_display = ('id', 'title', 'author')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Настройка отображения модели Post в админке"""
    list_display = ('id', 'title', 'author', 'publication_date', 'changed')
    list_display_links = ('id', 'title')
    readonly_fields = ('views', )


@admin.register(PostReaction)
class PostReactionAdmin(admin.ModelAdmin):
    """Настройка отображения модели PostReaction в админке"""
    list_display = ('id', 'content_type', 'profile', 'reaction')
    list_display_links = ('id', 'content_type')


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin, admin.ModelAdmin):
    """Настройка отображения модели Comment в админке"""
    list_display = ('profile', 'post', 'publication_date', 'id')
    list_display_links = ('profile', 'post')
    mptt_level_indent = 20
