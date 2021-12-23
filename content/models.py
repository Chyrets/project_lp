from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from profiles.models import Profile


def user_directory_path(instance, filename):
    return f'user_{instance.author.name}/{filename}'


class Tag(models.Model):
    """Модель тегов для поста"""
    title = models.CharField("Название", max_length=50)
    slug = models.SlugField("URL", null=False, unique=True)
    author = models.ForeignKey(
        Profile,
        verbose_name="Автор",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Post(models.Model):
    """Модель статей"""
    title = models.CharField("Заголовок", max_length=100)
    caption = models.TextField("Содержание", max_length=4000)
    picture = models.ImageField("Изображение", upload_to=user_directory_path, null=True, blank=True)
    publication_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    changed = models.BooleanField("Изменен", default=False)
    archived = models.BooleanField("В архиве", default=False)
    modification_date = models.DateTimeField('Дата изменения', auto_now=True, null=True, blank=True)
    views = models.IntegerField("Просмотры", default=0)
    tags = models.ManyToManyField(Tag, verbose_name="Теги", related_name='tags', blank=True)
    author = models.ForeignKey(Profile, verbose_name="Автор", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} by {self.author}'

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def get_absolute_url(self):
        return reverse('content:post_detail', args=str(self.id))
