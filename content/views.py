from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
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
            post = Post.objects.get(id=post_id, archived=False)
            post.views += 1
            post.save(update_fields=['views'])
            context['post'] = post
        except Post.DoesNotExist:
            raise Http404

        return context


class AddPostView(LoginRequiredMixin, FormView):
    """Страница для добавления нового поста"""
    form_class = AddPostForm
    template_name = 'content/add_post.html'
    success_url = reverse_lazy('profiles:home')
    login_url = reverse_lazy('profiles:login')

    def get_form_kwargs(self):
        kwargs = super(AddPostView, self).get_form_kwargs()
        # Добавляем аргумент user для конструктора класса AddPostForm
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        instance = form.save(commit=False)

        tag_form = form.cleaned_data.get('tags')
        author = form.cleaned_data.get('author')
        tag_objs = self.__add_new_tag(tag_form, author)

        instance.save()
        # Добавляем теги к созданному посту
        instance.tags.set(tag_objs)

        return redirect(self.get_success_url())

    @classmethod
    def __add_new_tag(cls, tag_form: str, author: str) -> list:
        """Создание новых тегов из строки введенной пользователем"""
        tag_objs = []
        tag_list = list(tag_form.replace(" ", "").split('#'))
        tag_list = [tag for tag in tag_list if len(tag) > 0]

        for tag in tag_list:
            t, created = Tag.objects.get_or_create(title=tag)
            if created:
                t.author = author
                t.save(update_fields=['author'])
            tag_objs.append(t)

        return tag_objs
