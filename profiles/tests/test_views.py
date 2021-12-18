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

    def test_view_url_accessible_by_name(self):
        """Проверка доступа к странице по имени profiles:login"""
        resp = self.client.get(reverse('profiles:login'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        """Проверка загружаемого template"""
        resp = self.client.get(reverse('profiles:login'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'profiles/login.html')

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


class RegisterUserTest(TestCase):
    """Тесты для класса отображения регистрации пользователя"""

    def setUp(self) -> None:
        self.credential = {'username': 'test_user', 'password1': 'TestPass2O', 'password2': 'TestPass2O'}
        self.crd_different_password = {'username': 'test_user2', 'password': 'TestPass2O', 'password2': 'TestPass21'}

    def test_signup_page_url(self):
        """Проверка адреса страницы регистрации"""
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/register.html')

    def test_signup_page_accessible_by_name(self):
        """Проверка доступа к странице регистрации по имени profiles:register"""
        response = self.client.get(reverse('profiles:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_user_correct_credential(self):
        """Проверка регистрации пользователя с правильными данными"""
        response = self.client.post(reverse('profiles:register'), data=self.credential)
        users_list = User.objects.all()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(users_list)

    def test_register_user_different_password(self):
        """Проверка регистрации пользователя с разными паролями"""
        response = self.client.get(reverse('profiles:register'), data=self.crd_different_password)
        users_list = User.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertFalse(users_list)

    def test_register_user_incorrect_username(self):
        """Проверка регистрации пользователя с существующим username"""
        User.objects.create_user(self.credential['username'], self.credential['password1'])
        response = self.client.post(reverse('profiles:register'), data=self.credential)
        users_list = User.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(users_list.count(), 1)
