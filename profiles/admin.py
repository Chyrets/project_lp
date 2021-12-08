from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    """Настройка отображения модели Profile в админке"""
    list_display = ('id', 'name', 'user')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Profile, ProfileAdmin)
