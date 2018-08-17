from django.test import TestCase
from django.urls import reverse


class SignUpView(TestCase):

    def test_user_create(self):
        user_data = {
            'username': 'tester1',
            'email': 'tester@example.com',
            'password1': '1234567890!',
            'password2': '1234567890!',
            'avatar': None
        }
        resp = self.client.post(
            reverse('profiles:signup'),
            data=user_data
        )
        self.assertRedirects(resp, reverse('main_page'))
