from django.contrib import admin

from .models import Follower


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    """Настройка отображения модели Follower в админке"""
    list_display = ('id', 'recipient', 'sender')
    list_display_links = ('recipient', 'sender')
