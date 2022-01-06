from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from content.models import Post, PostReaction
from content.services.view_services import add_remove_reaction
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
        self.assertTemplateUsed(response, 'content/add_or_edit_post.html')

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


class EditPostViewTest(TestCase):
    """Тесты для класса представления редактирования поста"""

    def setUp(self) -> None:
        test_user1 = User.objects.create_user(username='test_user1', password='password')
        test_user1.save()
        test_user2 = User.objects.create_user(username='test_user2', password='password')
        test_user2.save()
        profile = Profile.objects.first()
        self.test_post = Post.objects.create(
            title='test post1',
            caption='About test post1 by test_user1',
            author=profile
        )
        self.valid_data = {
            'title': 'test post1 dt',
            'caption': 'About test post1 dt',
            'tags': '#test_tag1',
            'author': profile.pk,
            'archived': True
        }
        self.invalid_data = {
            'title': '',
            'caption': 'About test post1 dt',
            'tags': '#test_tag1',
            'author': profile.pk,
            'archived': True
        }

    def test_redirect_if_not_logged_in(self):
        """Проверка перенаправления неавторизованного пользователя"""
        response = self.client.get(reverse('content:edit_post', kwargs={'post_id': self.test_post.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_logged_in_uses_correct_template(self):
        """Проверка отображения нужного шаблона для авторизованного пользователя"""
        self.client.login(username='test_user1', password='password')
        response = self.client.get(reverse('content:edit_post', kwargs={'post_id': self.test_post.pk}))

        self.assertEqual(str(response.context['user']), 'test_user1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'content/add_or_edit_post.html')

    def test_current_post_author(self):
        """Проверка того, что только автор поста может изменить его"""
        self.client.login(username='test_user2', password='password')
        response = self.client.get(reverse('content:edit_post', kwargs={'post_id': self.test_post.pk}))

        self.assertEqual(response.status_code, 404)

    def test_edit_post_with_valid_data(self):
        """Проверка метода form_valid"""
        self.client.login(username='test_user1', password='password')
        response = self.client.post(reverse('content:edit_post', kwargs={'post_id': self.test_post.pk}),
                                    data=self.valid_data)
        post = Post.objects.first()
        tag_list = post.tags.all()
        tags = ' '.join([f'#{tag.title}' for tag in tag_list])

        self.assertEqual(response.status_code, 302)
        self.assertEqual(post.title, 'test post1 dt')
        self.assertEqual(post.caption, 'About test post1 dt')
        self.assertEqual(tags, '#test_tag1')
        self.assertEqual(post.archived, True)


class PostReactionViewTest(TestCase):
    """Тесты для функционала добавления реакции"""

    def setUp(self) -> None:
        test_user1 = User.objects.create_user(username='test_user1', password='password')
        test_user1.save()
        self.profile = Profile.objects.first()
        self.test_post = Post.objects.create(
            title='test post1',
            caption='About test post1 by test_user1',
            author=self.profile
        )
        ct_post = ContentType.objects.get_for_model(Post)
        self.valid_data = {
            'profile': self.profile,
            'content_type': ct_post,
            'object_id': self.test_post.pk,
            'reaction': 1
        }

    def test_add_like_reaction(self):
        """Проверка добавления лайка к посту"""
        self.client.login(username='test_user1', password='password')
        response = self.client.get(
            reverse('content:post_reaction', kwargs={'post_id': self.test_post.pk, 'reaction': 1}))
        likes = PostReaction.objects.filter().count()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(likes, 1)

    def test_services_add_remove_reaction(self):
        """Проверка функции add_remove_reaction"""
        # Добавляем лайк
        add_remove_reaction(**self.valid_data)
        likes = PostReaction.objects.filter().count()
        self.assertEqual(likes, 1)

        # Меняем лайк на дизлайк
        self.valid_data['reaction'] = 2
        add_remove_reaction(**self.valid_data)
        dislike = PostReaction.objects.filter().count()
        self.assertEqual(dislike, 1)

        # Убираем дизлайк
        add_remove_reaction(**self.valid_data)
        dislike = PostReaction.objects.filter().count()
        self.assertEqual(dislike, 0)

        # Добавляем дизлайк
        add_remove_reaction(**self.valid_data)
        dislike = PostReaction.objects.filter().count()
        self.assertEqual(dislike, 1)
