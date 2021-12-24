from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView

from content.forms import AddPostForm
from content.models import Post, Tag
from profiles.models import Profile


class ProfilePostsView(TemplateView):
    """Страница с постами пользователя"""
    template_name = 'content/profile_posts_list.html'

    def get_context_data(self, profile_slug, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            author = Profile.objects.get(slug=profile_slug)
        except Profile.DoesNotExist:
            raise Http404

        context['profile_posts_list'] = Post.objects.filter(author=author, archived=False)

        return context


class PostDetailView(TemplateView):
    """Страница с отображением подробной информации поста"""
    template_name = 'content/post_detail.html'

    def get_context_data(self, post_id, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            post = Post.objects.get(id=int(post_id), archived=False)
            post.views += 1
            post.save(update_fields=['views'])
            context['post'] = post
        except Post.DoesNotExist:
            raise Http404

        return context


class AddPostView(FormView):
    """Страница для добавления нового поста"""
    form_class = AddPostForm
    template_name = 'content/add_post.html'
    success_url = reverse_lazy('profiles:home')

    def get_form_kwargs(self):
        kwargs = super(AddPostView, self).get_form_kwargs()
        # Добавляем аргумент user для конструктора класса AddPostForm
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        instance = form.save(commit=False)

        # Создаем недостающие теги из списка введенного пользователем
        tag_objs = []
        tag_form = form.cleaned_data.get('tags')
        tag_list = list(tag_form.replace(" ", "").split('#'))
        tag_list = [tag for tag in tag_list if len(tag) > 0]
        for tag in tag_list:
            t, created = Tag.objects.get_or_create(title=tag)
            if created:
                t.author = form.cleaned_data.get('author')
                t.save(update_fields=['author'])
            tag_objs.append(t)

        instance.save()
        # Добавляем теги к созданному посту
        instance.tags.set(tag_objs)

        return redirect(self.get_success_url())
