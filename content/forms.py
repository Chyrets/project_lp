from django import forms

from content.models import Post
from profiles.models import Profile


class AddPostForm(forms.ModelForm):
    """Форма добавления нового поста"""

    tags = forms.CharField(label=Post._meta.get_field('tags').verbose_name)

    def __init__(self, user, *args, **kwargs):
        super(AddPostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['caption'].widget.attrs.update({'class': 'form-control'})
        self.fields['picture'].widget.attrs.update({'class': 'form-control'})
        self.fields['archived'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['tags'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Каждый тег должен начинаться со знака #. (#тег1 #тег2)'
        })
        self.fields['author'].widget.attrs.update({'class': 'form-control'})
        self.fields['author'].queryset = Profile.objects.filter(user=user)

    class Meta:
        model = Post
        fields = ('title', 'caption', 'tags', 'picture', 'author', 'archived')
