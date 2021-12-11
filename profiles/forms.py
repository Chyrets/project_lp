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


class EditUserProfileForm(ModelForm):
    """Форма редактирования профиля пользователя"""

    def __init__(self, *args, **kwargs):
        super(EditUserProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Profile
        fields = ['name', 'about', 'birthday']

