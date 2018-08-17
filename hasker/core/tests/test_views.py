from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

from hasker.core.models import Question


class SearchRedirectViewTest(TestCase):

    def test_redirect(self):
        resp = self.client.post(reverse('search-redirect'), data={'search': 'test'})
        self.assertRedirects(resp, '/search/?q=test')
        resp = self.client.post(reverse('search-redirect'), data={'search': 'tag:tag1'})
        self.assertRedirects(resp, '/tag/tag1')


class CreateQuestionView(TestCase):

    def setUp(self):
        test_user1 = get_user_model().objects.create_user(
            username='testuser1',
            password='12345'
        )

    def test_question_create(self):
        self.client.login(username='testuser1', password='12345')
        question_data = {
            'tags': 'tag1, tag2, tag3',
            'title': 'some title',
            'text': 'some text'
        }
        resp = self.client.post(
            reverse('ask'),
            data=question_data
        )
        slug = slugify(question_data['title'])[:49]
        self.assertRedirects(resp, reverse('question', kwargs={'slug': slug}))
        Question.objects.get(slug=slug)