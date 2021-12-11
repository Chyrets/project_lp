from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile
from .forms import CustomUserCreationForm


def index(request):
    """Функция отображения для первичной домашней страницы сайта."""
    title = "Домашняя страница"
    content = {
        "title": title
    }

    return render(request, 'base.html', content)


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
            return redirect('home')
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
                return redirect('home')

        content = {'form': form}
        return render(request, self.template_name, content)


def logout_user(request):
    """Деавторизация пользователя"""
    logout(request)
    return redirect('login')


class UserProfilesView(LoginRequiredMixin, View):
    """Список профилей пользователя"""
    template_name = 'profiles/profiles_list.html'
    login_url = '/login/'

    def get(self, request):
        user = request.user
        profiles = Profile.objects.filter(user=user)

        context = {
            'profiles': profiles
        }
        return render(request, self.template_name, context)
