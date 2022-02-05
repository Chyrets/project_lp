from django import forms
from django.core.exceptions import ValidationError

from content.models import Post, Comment
from profiles.models import Profile


class TagWidgetMixin:
    def format_value(self, value):
        if value:
            value = ' '.join([f'#{tag.title}' for tag in value])
        else:
            value = None
        return super().format_value(value)


class TagWidget(TagWidgetMixin, forms.TextInput):
    pass


class TagField(forms.CharField):
    """Индивидуальное поле для поля tags модели Post"""
    widget = TagWidget

    def clean(self, value):
        value = super().clean(value)
        try:
            return value
        except ValueError:
            raise ValidationError(
                "Пожалуйста введите названия тегов в одну строку, каждый тег должен начинаться со знака #")

    def has_changed(self, initial_value, data_value):
        if self.disabled:
            return False

        try:
            data_value = self.clean(data_value)
        except forms.ValidationError:
            pass

        if not data_value:
            data_value = []
        if not initial_value:
            initial_value = []

        initial_value = [tag.name for tag in initial_value]
        initial_value.sort()

        return initial_value != data_value


class AddEditPostForm(forms.ModelForm):
    """Форма добавления, редактирования поста"""

    tags = TagField(label=Post._meta.get_field('tags').verbose_name)

    def __init__(self, user, *args, **kwargs):
        super(AddEditPostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['caption'].widget.attrs.update({'class': 'form-control'})
        self.fields['picture'].widget.attrs.update({'class': 'form-control'})
        self.fields['archived'].widget.attrs.update({'class': 'form-check-input'})

        # Настройка поля tags
        self.fields['tags'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Каждый тег должен начинаться со знака #. (#тег1 #тег2)'
        })
        self.fields['tags'].required = False

        self.fields['author'].widget.attrs.update({'class': 'form-control'})
        self.fields['author'].queryset = Profile.objects.filter(user=user)

    class Meta:
        model = Post
        fields = ('title', 'caption', 'tags', 'picture', 'author', 'archived')


class AddCommentForm(forms.ModelForm):
    """Форма добавления комментария"""

    class Meta:
        model = Comment
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(AddCommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
