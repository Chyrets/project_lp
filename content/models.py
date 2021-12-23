from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from profiles.models import Profile


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
