from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.text import slugify

from profiles.models import Profile
from ..models import Tag, Post


class TagModelTests(TestCase):
    """Тесты для модели Tag"""

    def setUp(self) -> None:
        User.objects.create(username='test_user', password='password')
        profile = Profile.objects.first()
        Tag.objects.create(title='test_tag', author=profile)

    def test_object_name_is_tag_title(self):
        """Проверка того, что имя объекта является именем тега"""
        tag = Tag.objects.first()
        expected_obj_name = f'{tag.title}'
        self.assertEqual(expected_obj_name, str(tag))

    def test_tag_slug_is_his_title(self):
        """Проверка того, что URL тега основа на его названии"""
        tag = Tag.objects.first()
        expected_tag_slug = slugify(tag.title)
        self.assertEqual(expected_tag_slug, tag.slug)


class PostModelTests(TestCase):
    """Тесты для модели Post"""

    def setUp(self) -> None:
        User.objects.create_user(username='test_user', password='password')
        profile = Profile.objects.first()
        Post.objects.create(title="post1", caption='About post1', author=profile)

    def test_object_name_is_post_title_by_author(self):
        """Проверка того, что имя объекта является именем поста и его автора"""
        post = Post.objects.first()
        expected_obj_name = f'{post.title} by {post.author}'
        self.assertEqual(expected_obj_name, str(post))
