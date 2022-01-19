from django.db import models
from django.contrib.auth.models import User


class Follower(models.Model):
    """Модель подписчиков"""
    recipient = models.ForeignKey(
        User,
        verbose_name="Адресат",
        on_delete=models.CASCADE,
        related_name='recipients',
    )
    sender = models.ForeignKey(
        User,
        verbose_name="Адресант",
        on_delete=models.CASCADE,
        related_name='senders'
    )

    def __str__(self):
        return f'{self.recipient} followed by {self.sender}'

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "подписчики"
