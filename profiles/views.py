from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .models import Profile
from .forms import CustomUserCreationForm, UserProfileForm


class LoginUserView(View):
    """Авторизация пользователя"""
    template_name = 'profiles/login.html'

    def get(self, request):
        """Отображение страницы авторизации пользователя"""
        return render(request, self.template_name)

    def post(self, request):
        """Обработка страницы авторизации пользователя"""
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('content:home')
        else:
            content = {
                "error": 'Неверные имя пользователя или пароль'
            }

        return render(request, self.template_name, content)


class RegisterUserView(View):
    """Регистрация пользователя"""
    template_name = 'profiles/register.html'
    form = CustomUserCreationForm

    def get(self, request):
        """Отображение страницы регистрации пользователя"""
        content = {'form': self.form}
        return render(request, self.template_name, content)

    def post(self, request):
        """Обработка страницы регистрации пользователя"""
        form = self.form(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('content:home')

        content = {'form': form}
        return render(request, self.template_name, content)


def logout_user(request):
    """Деавторизация пользователя"""
    logout(request)
    return redirect('profiles:login')


class UserProfilesView(LoginRequiredMixin, View):
    """Список профилей пользователя"""
    template_name = 'profiles/profiles_list.html'

    def get_login_url(self):
        """Перенаправляет на страницу авторизации, если пользователь не авторизован"""
        return reverse('profiles:login')

    def get(self, request):
        """Отображение списка профилей пользователя"""
        user = request.user
        profiles = Profile.objects.filter(user=user)

        try:
            profile = Profile.objects.get(user=user, used=True)
        except Profile.MultipleObjectsReturned:
            profile = Profile.objects.filter(user=user, used=True).first()

        context = {
            'profiles': profiles,
            'used_profile': profile
        }
        return render(request, self.template_name, context)


class AllProfilesView(TemplateView):
    """Отображение списка всех профилей"""
    template_name = 'profiles/all_profiles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        try:
            profile = Profile.objects.get(user=user, used=True)
        except Profile.MultipleObjectsReturned:
            profile = Profile.objects.filter(user=user, used=True).first()

        profiles = Profile.objects.all()

        context['used_profile'] = profile
        context['profiles'] = profiles

        return context


class AddUserProfileView(LoginRequiredMixin, View):
    """Добавление нового профиля пользователя"""
    template_name = 'profiles/add_profile.html'
    form = UserProfileForm

    def get_login_url(self):
        """Перенаправляет на страницу авторизации, если пользователь не авторизован"""
        return reverse('profiles:login')

    def get(self, request):
        """Отображение формы для добавления нового профиля"""
        user = request.user

        try:
            profile = Profile.objects.get(user=user, used=True)
        except Profile.MultipleObjectsReturned:
            profile = Profile.objects.filter(user=user, used=True).first()

        context = {
            'form': self.form(),
            'used_profile': profile
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """Обработка формы добавления профиля"""
        user = request.user
        form = self.form(request.POST)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()

            return redirect('profiles:profiles')

        context = {
            'form': form
        }

        return render(request, self.template_name, context)


class EditUserProfileView(LoginRequiredMixin, View):
    """Редактирование профиля пользователя"""
    template_name = 'profiles/edit_profile.html'
    form = UserProfileForm

    def get_login_url(self):
        """Перенаправляет на страницу авторизации, если пользователь не авторизован"""
        return reverse('profiles:login')

    def get(self, request, profile_slug):
        """Отображение информации профиля по его slug"""
        user = request.user
        profile = Profile.objects.get(slug=profile_slug, user=user)
        form = self.form(instance=profile)

        try:
            used_profile = Profile.objects.get(user=user, used=True)
        except Profile.MultipleObjectsReturned:
            used_profile = Profile.objects.filter(user=user, used=True).first()

        context = {
            'profile': profile,
            'form': form,
            'used_profile': used_profile
        }

        return render(request, self.template_name, context)

    def post(self, request, profile_slug):
        """Изменение профиля"""
        user = request.user
        profile = Profile.objects.get(slug=profile_slug, user=user)
        form = self.form(request.POST, instance=profile)

        if form.is_valid():
            profile = form.save()

        context = {
            'profile': profile,
            'form': form
        }

        return render(request, self.template_name, context)


class DeleteUserProfile(LoginRequiredMixin, View):
    """Удаление профиля пользователя"""
    template_name = 'profiles/delete_profile.html'

    def get_login_url(self):
        """Перенаправляет на страницу авторизации, если пользователь не авторизован"""
        return reverse('profiles:login')

    def get(self, request, profile_slug):
        """Отображение информации об профиле, который собираются удалить"""
        user = request.user
        profile = Profile.objects.get(slug=profile_slug, user=user)

        try:
            used_profile = Profile.objects.get(user=user, used=True)
        except Profile.MultipleObjectsReturned:
            used_profile = Profile.objects.filter(user=user, used=True).first()

        context = {
            'profile': profile,
            'used_profile': used_profile
        }

        return render(request, self.template_name, context)

    def post(self, request, profile_slug):
        """Обработка запроса удаления профиля"""
        user = request.user
        profile = Profile.objects.get(slug=profile_slug, user=user)

        profile.delete()

        return redirect('profiles:profiles')
