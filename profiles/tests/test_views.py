from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LoginUserTest(TestCase):
    """Тест класса авторизации пользователя"""
    def setUp(self) -> None:
        self.credential = {'username': 'test_user', 'password': 'password'}
        self.crd_incorrect_username = {'username': 'test_user2', 'password': 'password'}
        self.crd_incorrect_password = {'username': 'test_user', 'password': 'password3'}
        User.objects.create_user(**self.credential)

    def test_login_correct_username_and_password(self):
        """Проверка авторизации пользователя с правильными данными"""
        response = self.client.post(reverse('profiles:login'), self.credential, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_incorrect_username(self):
        """Проверка авторизации пользователя с неправильным username"""
        response = self.client.post(reverse('profiles:login'), self.crd_incorrect_username, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_login_incorrect_password(self):
        """Проверка авторизации пользователя с неправильным password"""
        response = self.client.post(reverse('profiles:login'), self.crd_incorrect_password, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)


