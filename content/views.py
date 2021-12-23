from django.shortcuts import render
from django.views.generic import TemplateView

from content.models import Post


class ProfilePostsView(TemplateView):
    """Страница с постами пользователя"""
    template_name = 'content/profile_posts_list.html'

    def get_context_data(self, profile_slug, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_posts_list'] = Post.objects.filter(author__name=profile_slug, archived=False)
        return context
