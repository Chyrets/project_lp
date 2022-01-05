from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    """Создание профиля для нового пользователя"""
    if created:
        Profile.objects.create(name=instance.username, user=instance, used=True)


@receiver(post_save, sender=Profile)
def change_used_profile(sender, instance, **kwargs):
    """Изменение используемого аккаунта"""
    Profile.objects.filter(used=True, user=instance.user).update(used=False)
    Profile.objects.filter(pk=instance.pk).update(used=True)
