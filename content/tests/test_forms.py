from django.contrib.auth.models import User
from django.test import TestCase

from ..forms import AddEditPostForm


class AddPostFormTest(TestCase):
    """Тесты для формы добавления нового поста"""

    def setUp(self) -> None:
        self.test_user = User.objects.create_user(username='test_user', password='password')

    def test_form_fields_label_text(self):
        """Проверка значения label полей формы"""
        form = AddEditPostForm(self.test_user)

        self.assertEqual(form.fields['title'].label, 'Заголовок')
        self.assertEqual(form.fields['caption'].label, 'Содержание')
        self.assertEqual(form.fields['picture'].label, 'Изображение')
        self.assertEqual(form.fields['archived'].label, 'В архиве')
        self.assertEqual(form.fields['tags'].label, 'Теги')
        self.assertEqual(form.fields['author'].label, 'Автор')
