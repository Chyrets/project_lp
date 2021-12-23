from django.contrib import admin

from .models import Tag, Post


class TagAdmin(admin.ModelAdmin):
    """Настройка отображения модели Tag в админке"""
    list_display = ('id', 'title', 'author')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}


class PostAdmin(admin.ModelAdmin):
    """Настройка отображения модели Post в админке"""
    list_display = ('id', 'title', 'author', 'publication_date', 'changed')
    list_display_links = ('id', 'title')
    readonly_fields = ('views', )


admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
