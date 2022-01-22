from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, DeleteView
from django.db.models import Q, Count

from content.forms import AddEditPostForm, AddCommentForm
from content.models import Post, PostReaction, Comment
from content.services.view_services import add_new_tag, add_remove_reaction
from profiles.models import Profile


class MasterView(TemplateView):
    """Отображение первичной страницы"""
    template_name = 'content/master.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'TyWe'

        return context


class HomeView(LoginRequiredMixin, TemplateView):
    """Главная страница для авторизованных пользователей"""
    template_name = 'content/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        try:
            profile = Profile.objects.get(user=user, used=True)
        except Profile.MultipleObjectsReturned:
            profile = Profile.objects.filter(user=user, used=True).first()

        recipients_posts = Post.objects.filter(
            author__recipients__sender=profile
        ).annotate(
            likes=Count('reaction', filter=Q(reaction__reaction=PostReaction.LIKE)),
            dislikes=Count('reaction', filter=Q(reaction__reaction=PostReaction.DISLIKE))
        ).prefetch_related(
            'tags'
        ).select_related(
            'author'
        ).prefetch_related('comments')
        profile_posts = Post.objects.filter(author=profile)
        posts = (recipients_posts | profile_posts).order_by('-publication_date')

        context['posts'] = posts

        return context


class PostsByTagView(TemplateView):
    """Вывод постов по их хэштегу"""
    template_name = 'content/posts_by_tag.html'

    def get_context_data(self, tag, **kwargs):
        context = super().get_context_data(**kwargs)

        posts = Post.objects.filter(
            tags__slug__contains=tag
        ).annotate(
            likes=Count('reaction', filter=Q(reaction__reaction=PostReaction.LIKE)),
            dislikes=Count('reaction', filter=Q(reaction__reaction=PostReaction.DISLIKE))
        ).order_by('-publication_date')

        context['posts'] = posts

        return context


class ProfilePostsView(TemplateView):
    """Страница с постами пользователя"""
    template_name = 'content/profile_posts_list.html'

    def get_context_data(self, profile_slug, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            author = Profile.objects.get(slug=profile_slug)
        except Profile.DoesNotExist:
            raise Http404

        context['profile_posts_list'] = Post.objects.filter(author=author, archived=False).prefetch_related('comments')
        context['profile'] = author

        return context


class PostDetailView(TemplateView):
    """Страница с отображением подробной информации поста"""
    template_name = 'content/post_detail.html'

    def get_context_data(self, post_id, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            post = Post.objects.prefetch_related(
                'author__user'
            ).annotate(
                likes=Count('reaction', filter=Q(reaction__reaction=PostReaction.LIKE)),
                dislikes=Count('reaction', filter=Q(reaction__reaction=PostReaction.DISLIKE))
            ).get(id=post_id, archived=False)
        except Post.DoesNotExist:
            raise Http404

        comments = Comment.objects.filter(post=post).select_related('profile').select_related('profile__user')
        form = AddCommentForm()

        post.views += 1
        post.save(update_fields=['views'])

        context['post'] = post
        context['likes'] = post.likes
        context['dislikes'] = post.dislikes
        context['comments'] = comments
        context['form'] = form

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


class PostReactionView(LoginRequiredMixin, View):
    """Функционал для кнопок лайков/дизлайков поста"""
    login_url = reverse_lazy('profiles:login')

    def get(self, request, post_id, reaction):
        user = request.user
        ct_post = ContentType.objects.get_for_model(Post)

        # Получаем основной профиль пользователя
        try:
            profile = Profile.objects.get(user=user, used=True)
        except Profile.MultipleObjectsReturned:
            profile = Profile.objects.filter(user=user, used=True).first()

        # Достаем из бд пост с текущей страницы
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise Http404

        # Обрабатываем реакцию пользователя
        add_remove_reaction(profile, ct_post, post.pk, reaction)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AddCommentView(LoginRequiredMixin, View):
    """Отображение формы добавления комментария"""
    login_url = reverse_lazy('profile:login')
    form = AddCommentForm

    def get_success_url(self):
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def post(self, request, post_id):
        user = request.user
        form = self.form(request.POST)

        try:
            profile = Profile.objects.get(user=user, used=True)
        except Profile.MultipleObjectsReturned:
            profile = Profile.objects.filter(user=user, used=True).first()

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise Http404

        if form.is_valid():
            comment = form.save(commit=False)
            comment.text = request.POST['text']
            comment.profile = profile
            comment.post = post

            if request.POST.get("parent", None):
                comment.parent_id = int(request.POST.get("parent"))

            comment.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class EditCommentView(LoginRequiredMixin, View):
    """Отображение функционала изменения комментария"""
    login_url = reverse_lazy('profile:login')

    def get_success_url(self):
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            raise Http404

        text = request.POST['text']
        comment.text = text
        comment.changed = True
        comment.save(update_fields=['text', 'changed', 'modification_date'])

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteCommentView(LoginRequiredMixin, View):
    """Отображение функционала для удаления комментария"""
    model = Comment
    login_url = reverse_lazy('profiles:login')

    def get_success_url(self):
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            raise Http404

        comment.deleted = True
        comment.save(update_fields=['deleted'])

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
