from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    """Создание профиля для нового пользователя"""
    if created:
        Profile.objects.create(name=instance.username, user=instance)
