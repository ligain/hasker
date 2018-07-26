from io import BytesIO

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.conf import settings

from PIL import Image


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Enter a valid email address.')
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'avatar')

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        image = Image.open(avatar.file)
        output = BytesIO()

        resized_img = image.resize(settings.AVATAR_SIZE)
        resized_img.save(output, format=avatar.image.format, quality=100)

        avatar.file = output
        avatar.image = resized_img
        return avatar
