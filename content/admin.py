from django.contrib import admin

from .models import Tag


class TagAdmin(admin.ModelAdmin):
    """Настройка отображения модели Tag в админке"""
    list_display = ('id', 'title', 'author')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Tag, TagAdmin)
