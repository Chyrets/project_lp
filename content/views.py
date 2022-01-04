from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, DeleteView

from content.forms import AddEditPostForm
from content.models import Post
from content.services.view_services import add_new_tag
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
    form_class = AddEditPostForm
    template_name = 'content/add_or_edit_post.html'
    success_url = reverse_lazy('profiles:home')
    login_url = reverse_lazy('profiles:login')

    def get_form_kwargs(self):
        kwargs = super(AddPostView, self).get_form_kwargs()
        # Добавляем аргумент user для конструктора класса AddPostForm
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        instance = form.save(commit=False)

        # получение списка тегов и автора
        tag_form = form.cleaned_data.get('tags')
        author = form.cleaned_data.get('author')

        # Добавление новых тегов в бд и создание списка тегов для поста
        tag_objs = add_new_tag(tag_form, author)

        instance.save()
        # Добавляем теги к созданному посту
        instance.tags.set(tag_objs)

        return redirect(self.get_success_url())


class EditPostView(LoginRequiredMixin, FormView):
    """Страница редактирования поста"""
    form_class = AddEditPostForm
    template_name = 'content/add_or_edit_post.html'
    login_url = reverse_lazy('profiles:login')
    success_url = reverse_lazy('profiles:home')

    def get_form_kwargs(self):
        kwargs = super(EditPostView, self).get_form_kwargs()
        # Добавляем аргумент user для конструктора класса AddPostForm
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        try:
            post = Post.objects.get(pk=self.kwargs['post_id'], author__user=user)
        except Post.DoesNotExist:
            raise Http404

        context['form'] = self.form_class(instance=post, user=self.request.user)
        return context

    def form_valid(self, form):
        post_id = self.kwargs['post_id']
        user = self.request.user
        post = Post.objects.get(pk=post_id, author__user=user)

        tag_form = form.cleaned_data.get('tags')
        author = form.cleaned_data.get('author')

        tag_objs = add_new_tag(tag_form, author)

        # Добавление тегов к посту
        post.tags.set(tag_objs)
        # обновление полей модели
        post.title = form.cleaned_data['title']
        post.caption = form.cleaned_data['caption']
        post.picture = form.cleaned_data['picture']
        post.author = form.cleaned_data['author']
        post.archived = form.cleaned_data['archived']
        post.save(update_fields=['title', 'caption', 'picture', 'author', 'archived'])

        return redirect(self.get_success_url())


class DeletePostView(LoginRequiredMixin, DeleteView):
    """Страница для подтверждения удаления поста"""
    model = Post
    template_name = 'content/delete_post.html'
    success_url = reverse_lazy('profiles:home')
    login_url = reverse_lazy('profiles:login')

    def get_object(self, queryset=None):
        """Проверка того, что автор поста текущий пользователь"""
        post = super(DeletePostView, self).get_object()

        if not post.author.user == self.request.user:
            raise Http404

        return post
