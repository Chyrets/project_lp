from django.test import TestCase

from ..forms import CustomUserCreationForm


class CustomUserCreationFormTest(TestCase):
    """Тесты для формы создания пользователя"""

    def test_form_username_field_label(self):
        """Проверка текста поля label"""
        form = CustomUserCreationForm()
        self.assertEqual(form.fields['username'].label, 'Имя пользователя')
