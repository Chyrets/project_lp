from django.db import models

from profiles.models import Profile


class Follower(models.Model):
    """Модель подписчиков"""
    recipient = models.ForeignKey(
        Profile,
        verbose_name="Адресат",
        on_delete=models.CASCADE,
        related_name='recipients',
    )
    sender = models.ForeignKey(
        Profile,
        verbose_name="Адресант",
        on_delete=models.CASCADE,
        related_name='senders'
    )

    def __str__(self):
        return f'{self.recipient} followed by {self.sender}'

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "подписчики"
