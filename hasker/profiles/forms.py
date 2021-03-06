from io import BytesIO

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.conf import settings

from PIL import Image


class AvatarMixin:
    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        if avatar:
            image = Image.open(avatar.file)
            output = BytesIO()

            resized_img = image.resize(settings.AVATAR_SIZE)
            resized_img.save(output, format=avatar.image.format, quality=100)

            avatar.file = output
            avatar.image = resized_img

        return avatar


class SignUpForm(AvatarMixin, UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Enter a valid email address.')
    avatar = forms.ImageField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'avatar')


class SettingsForm(AvatarMixin, forms.ModelForm):
    email = forms.EmailField(max_length=255, required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('email', 'avatar')
