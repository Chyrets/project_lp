from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Profile


class ProfileModelTests(TestCase):
    """Тесты для модели Profile"""

    def setUp(self) -> None:
        self.user = User.objects.create(username='test_user', password='password')

    def test_create_user_profile_for_new_user(self):
        """Проверка создания профиля для новых пользователей"""
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.name, self.user.username)
        self.assertEqual(profile.user, self.user)

