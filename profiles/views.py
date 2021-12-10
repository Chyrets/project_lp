from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View

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
