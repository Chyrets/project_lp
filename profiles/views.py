from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View


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
