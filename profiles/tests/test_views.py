from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from profiles.models import Profile


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
        user_list = User.objects.all()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(user_list)

    def test_register_user_different_password(self):
        """Проверка регистрации пользователя с разными паролями"""
        response = self.client.get(reverse('profiles:register'), data=self.crd_different_password)
        user_list = User.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertFalse(user_list)

    def test_register_user_incorrect_username(self):
        """Проверка регистрации пользователя с существующим username"""
        User.objects.create_user(self.credential['username'], self.credential['password1'])
        response = self.client.post(reverse('profiles:register'), data=self.credential)
        users_list = User.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(users_list.count(), 1)


class UserProfilesTest(TestCase):
    """Тесты для класса просмотра профилей пользователя"""

    def setUp(self):
        test_user1 = User.objects.create_user(username='test_user1', password='password')
        test_user1.save()

        number_of_profiles = 10
        for profile in range(number_of_profiles):
            Profile.objects.create(user=test_user1)

    def test_redirect_if_not_logged_in(self):
        """Перенаправление если пользователь не авторизован"""
        response = self.client.get(reverse('profiles:profiles'))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_uses_correct_template(self):
        """Проверка отображения нужного template для авторизованного пользователя"""
        # авторизация пользователя
        self.client.login(username='test_user1', password='password')
        response = self.client.get(reverse('profiles:profiles'))

        # проверка, что пользователь авторизовался
        self.assertEqual(str(response.context['user']), 'test_user1')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profiles_list.html')

    def test_profile_list_display(self):
        """Отображение списка профилей авторизованного пользователя"""
        self.client.login(username='test_user1', password='password')
        response = self.client.get(reverse('profiles:profiles'))

        profile_list = Profile.objects.filter(user=response.context['user'])

        self.assertEqual(profile_list.count(), 11)


class AddUserProfileTest(TestCase):
    """Тесты для класса добавления нового профиля"""

    def setUp(self) -> None:
        test_user1 = User.objects.create_user(username='test_user1', password='password')
        test_user1.save()
        test_user2 = User.objects.create_user(username='test_user2', password='password')
        test_user2.save()

        self.valid_data = {'name': 'test_profile1',
                           'about': 'About test profile1',
                           'birthday': '2002-01-01',
                           'user': test_user1}
        self.invalid_birthday = {'name': 'test_profile1',
                                 'about': 'About test profile1',
                                 'birthday': '2002.10-01',
                                 'user': test_user1}
        self.invalid_user = {'name': 'test_profile1',
                             'about': 'About test profile1',
                             'birthday': '2002-01-01',
                             'user': test_user2}

    def test_redirect_if_not_logged_in(self):
        """Проверка перенаправления неавторизованного пользователя"""
        response = self.client.get(reverse('profiles:add_profile'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_logged_in_uses_correct_template(self):
        """Проверка отображения нужного template для авторизованного пользователя"""
        self.client.login(username='test_user1', password='password')
        response = self.client.get(reverse('profiles:add_profile'))

        self.assertEqual(str(response.context['user']), 'test_user1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/add_profile.html')

    def test_create_user_profile_with_valid_data(self):
        """Проверка создания профиля с корректными данными"""
        self.client.login(username='test_user1', password='password')
        response = self.client.post(reverse('profiles:add_profile'), data=self.valid_data)
        profile_list = Profile.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profiles:profiles'))
        # Длина будет равна трем, так как один профиль создаются автоматически при регистрации пользователя
        self.assertEqual(len(profile_list), 3)

    def test_create_user_profile_with_invalid_birthday(self):
        """Проверка создания профиля с некорректной датой"""
        self.client.login(username='test_user1', password='password')
        response = self.client.post(reverse('profiles:add_profile'), data=self.invalid_birthday)
        profile_list = Profile.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(profile_list), 2)


class EditUserProfileTest(TestCase):
    """Тесты для класса редактирования профиля"""

    def setUp(self) -> None:
        test_user1 = User.objects.create_user(username='test_user1', password='password')
        test_user1.save()
        user_data = {'name': 'test_profile1',
                     'about': 'About test profile1',
                     'birthday': '2002-01-01',
                     'user': test_user1}
        self.test_profile1 = Profile.objects.create(**user_data)
        self.valid_data = {'name': 'test_profile1_1',
                           'about': 'About test profile1_1',
                           'birthday': '2002-01-02', }
        self.invalid_birthday = {'name': 'test_profile1',
                                 'about': 'About test profile1',
                                 'birthday': '2002.01-01'}

    def _login_user(self, username: str, password: str) -> bool:
        """Авторизовать пользователя"""
        return self.client.login(username=username, password=password)

    def _get_response(self, type_data):
        """Получить ответ от метода post"""
        if type_data == self.valid_data:
            response = self.client.post(
                reverse('profiles:edit_profile', kwargs={'profile_slug': self.test_profile1.slug}),
                data=self.valid_data
            )
        else:
            response = self.client.post(
                reverse('profiles:edit_profile', kwargs={'profile_slug': self.test_profile1.slug}),
                data=self.invalid_birthday
            )
        return response

    def test_redirect_if_not_logged_in(self):
        """Проверка перенаправления неавторизованного пользователя"""
        response = self.client.get(reverse('profiles:edit_profile', kwargs={'profile_slug': self.test_profile1.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_logged_in_uses_correct_template(self):
        """Проверка отображения нужного template для авторизованного пользователя"""
        self.client.login(username='test_user1', password='password')
        response = self.client.get(reverse('profiles:edit_profile', kwargs={'profile_slug': self.test_profile1.slug}))

        self.assertEqual(str(response.context['user']), 'test_user1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/edit_profile.html')

    def test_edit_user_profile_with_valid_data(self):
        """Проверка редактирования профиля с корректными данными"""
        self._login_user('test_user1', 'password')
        response = self._get_response(self.valid_data)
        profile = Profile.objects.get(slug=self.test_profile1.slug)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(profile.name, 'test_profile1_1')
        self.assertEqual(profile.about, 'About test profile1_1')
        self.assertEqual(profile.birthday.strftime('%Y-%m-%d'), '2002-01-02')

    def test_edit_user_with_invalid_birthday(self):
        """Проверка редактирования пользователя с некорректной датой"""
        self._login_user('test_user1', 'password')
        response = self._get_response(self.invalid_birthday)
        profile = Profile.objects.get(slug=self.test_profile1.slug)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(profile.name, 'test_profile1')
        self.assertEqual(profile.about, 'About test profile1')
        self.assertEqual(profile.birthday.strftime('%Y-%m-%d'), '2002-01-01')


class DeleteUserProfileTest(TestCase):
    """Тесты для класса удаления профиля"""

    def setUp(self) -> None:
        test_user1 = User.objects.create_user(username='test_user1', password='password')
        test_user1.save()
        user_data = {'name': 'test_profile1',
                     'about': 'About test profile1',
                     'birthday': '2002-01-01',
                     'user': test_user1}
        self.test_profile1 = Profile.objects.create(**user_data)

    def test_redirect_if_not_logged_in(self):
        """Проверка перенаправления неавторизованного пользователя"""
        response = self.client.get(reverse('profiles:delete_profile', kwargs={'profile_slug': self.test_profile1.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_logged_in_uses_correct_template(self):
        """Проверка отображения нужного template для авторизованного пользователя"""
        self.client.login(username='test_user1', password='password')
        response = self.client.get(reverse('profiles:delete_profile', kwargs={'profile_slug': self.test_profile1.slug}))

        self.assertEqual(str(response.context['user']), 'test_user1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/delete_profile.html')

    def test_delete_user_profile(self):
        """Проверка удаления профиля пользователя"""
        user = self.client.login(username='test_user1', password='password')
        response = self.client.post(
            reverse('profiles:delete_profile', kwargs={'profile_slug': self.test_profile1.slug}))
        profile_list = Profile.objects.filter(user=user)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profiles:profiles'))

        self.assertEqual(len(profile_list), 1)
