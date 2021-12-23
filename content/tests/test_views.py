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

    def test_view_uses_correct_template(self):
        """Проверка отображения нужного template"""
        response = self.client.get(reverse('content:profile_posts_list', kwargs={'profile_slug': self.profile1.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'content/profile_posts_list.html')
