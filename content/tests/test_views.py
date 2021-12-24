from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from content.models import Post
from profiles.models import Profile


class ProfilePostsTest(TestCase):
    """Тесты для класса отображения постов пользователя по его имени"""

    def setUp(self) -> None:
        test_user1 = User.objects.create_user(username='test_user1', password='password')
        test_user1.save()
        self.profile1 = Profile.objects.first()

        number_of_posts = 10
        for post in range(number_of_posts):
            if post % 2:
                archived = True
            else:
                archived = False
            Post.objects.create(
                title=f'Test post{post}',
                caption=f'Test caption post{post}',
                archived=archived,
                author=self.profile1
            )

    def test_view_uses_correct_template(self):
        """Проверка отображения нужного template"""
        response = self.client.get(reverse('content:profile_posts_list', kwargs={'profile_slug': self.profile1.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'content/profile_posts_list.html')

    def test_raise_404_for_page_with_wrong_slug(self):
        """Проверка возвращения 404 ошибки для страницы с неправильным slug"""
        response = self.client.get(reverse('content:profile_posts_list', kwargs={'profile_slug': 'wrong_slug'}))

        self.assertEqual(response.status_code, 404)

    def test_display_correct_number_of_posts(self):
        """Проверка отображения правильного количества постов"""
        profile_posts_list = Post.objects.filter(author=self.profile1, archived=False)

        self.assertTrue(len(profile_posts_list), 5)


class PostDetailTest(TestCase):
    """Тесты для класса отображения полной информации поста по его id"""

    def setUp(self) -> None:
        test_user1 = User.objects.create_user(username='test_user1', password='password')
        test_user1.save()
        self.profile1 = Profile.objects.first()
        self.post1 = Post.objects.create(
            title='test post1',
            caption='About test post1',
            author=self.profile1
        )

    def test_view_uses_correct_template(self):
        """Проверка отображения нужного template"""
        response = self.client.get(reverse('content:post_detail', kwargs={'post_id': self.post1.id}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'content/post_detail.html')

    def test_raise_404_for_page_with_wrong_slug(self):
        """Проверка возвращения 404 ошибки для страницы с неправильным post_id"""
        response = self.client.get(reverse('content:post_detail', kwargs={'post_id': 0}))

        self.assertEqual(response.status_code, 404)

    def test_add_one_view_when_page_load(self):
        """Проверка счетчика просмотров, при загрузке страницы он должен увеличиться на один"""
        response = self.client.get(reverse('content:post_detail', kwargs={'post_id': self.post1.id}))

        self.assertEqual(response.context['post'].views, 1)


class AddPostViewTest(TestCase):
    """Тесты для класса добавления нового профиля"""

    def setUp(self) -> None:
        test_user1 = User.objects.create_user(username='test_user1', password='password')
        test_user1.save()
        self.profile1 = Profile.objects.first()
        self.valid_data = {
            'title': 'test post1',
            'caption': 'About test post1',
            'tags': '#tag1 #tag2',
            'author': self.profile1.pk
        }
        self.invalid_title = {
            'title': '',
            'caption': 'About test post1',
            'tags': '#tag1 #tag2',
            'author': self.profile1.pk
        }

    def test_redirect_if_not_logged_in(self):
        """Проверка перенаправления неавторизованного пользователя"""
        response = self.client.get(reverse('content:add_post'))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_logged_in_uses_correct_template(self):
        """Проверка отображения нужного шаблона для авторизованного пользователя"""
        self.client.login(username='test_user1', password='password')
        response = self.client.get(reverse('content:add_post'))

        self.assertEqual(str(response.context['user']), 'test_user1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'content/add_post.html')

    def test_add_post_with_valid_data(self):
        """Проверка добавления поста с правильными данными"""
        self.client.login(username='test_user1', password='password')
        response = self.client.post(reverse('content:add_post'), data=self.valid_data)
        post_list = Post.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profiles:home'))
        self.assertEqual(len(post_list), 1)

    def test_add_post_with_invalid_title(self):
        """Проверка добавления поста с пустым полем заголовка"""
        self.client.login(username='test_user1', password='password')
        response = self.client.post(reverse('content:add_post'), data=self.invalid_title)
        post_list = Post.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(post_list), 0)
