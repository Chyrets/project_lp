from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации пользователя"""

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control',
                                                     'placeholder': 'Введите имя пользователя'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'подтвердите пароль'})


class UserProfileForm(ModelForm):
    """Форма добавления и редактирования профиля пользователя"""

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name != "used":
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': "form-check-input"})

    class Meta:
        model = Profile
        fields = ['name', 'about', 'birthday', 'used']

