import random
import string

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


def rand_slug() -> str:
    """Создание случайной строки для поля slug"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))


class Profile(models.Model):
    """Модель профиля пользователя"""
    name = models.CharField('Имя', max_length=100)
    about = models.TextField('О себе', max_length=500, blank=True, null=True)
    birthday = models.DateField('День рождения', blank=True, null=True)
    avatar = models.ImageField('Фотография', upload_to='user/avatar', blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='profile')
    slug = models.SlugField('URL', unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.name}-{rand_slug()}')
        super(Profile, self).save(*args, **kwargs)
