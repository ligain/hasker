from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class APITest(APITestCase):
    fixtures = ['initial_data.json']
    highest_rating = 4

    def setUp(self):
        tester1 = get_user_model().objects.create(
            username='tester1',
            email='tester1@example.com',
            password='123123*&^'
        )
        self.client.force_authenticate(user=tester1)

    def test_main_page(self):
        questions_on_main_page = 7

        url = reverse('api1:main-page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), questions_on_main_page)

    def test_main_page_hot_questions(self):
        url = reverse('api1:main-page')
        response = self.client.get(url, data={'order_by': 'hot'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['rating'], self.highest_rating)

    def test_one_question(self):
        question_slug = 'pass-data-from-class-select-to-get-route'

        url = reverse('api1:questions', kwargs={'slug': question_slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], question_slug)

    def test_trending(self):
        url = reverse('api1:trending')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['rating'], self.highest_rating)

    def test_answers_for_question(self):
        question_slug = 'pass-data-from-class-select-to-get-route'
        answers_in_question = 1
        rating_for_answer = 1

        url = reverse('api1:answers-for-question', kwargs={'slug': question_slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], answers_in_question)
        self.assertEqual(response.data['results'][0]['rating'], rating_for_answer)

    def test_search_by_string(self):
        search_string = 'pass'
        found_questions = 1
        found_question_slug = 'pass-data-from-class-select-to-get-route'

        url = reverse('api1:search-by-string', kwargs={'q': search_string})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], found_questions)
        self.assertEqual(response.data['results'][0]['slug'], found_question_slug)

    def test_search_by_tag(self):
        search_tag = 'python'
        found_questions = 3

        url = reverse('api1:search-by-tag', kwargs={'tag': search_tag})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], found_questions)

    def test_search_by_empty_tag(self):
        search_tag = 'wrong-tag'
        questions_with_wrong_tag = 0

        url = reverse('api1:search-by-tag', kwargs={'tag': search_tag})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], questions_with_wrong_tag)
