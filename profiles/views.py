from django.shortcuts import render


def index(request):
    """Функция отображения для первичной домашней страницы сайта."""
    title = "Домашняя страница"
    content = {
        "title": title
    }

    return render(request, 'base.html', content)
