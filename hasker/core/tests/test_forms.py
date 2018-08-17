import random
import string

from django.test import TestCase

from hasker.core.forms import CreateQuestionForm, QueryForm


class CreateQuestionFormTest(TestCase):

    def test_invalid_tags(self):
        form_data = {
            'tags': 'sometag',
            'title': 'some title',
            'text': 'some text'
        }
        form = CreateQuestionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_tags(self):
        form_data = {
            'tags': 'tag1, tag2, tag3',
            'title': 'some title',
            'text': 'some text'
        }
        form = CreateQuestionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_absent_text_field(self):
        form_data = {
            'tags': 'tag1, tag2, tag3',
            'title': 'some title',
        }
        form = CreateQuestionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_absent_title_field(self):
        form_data = {
            'tags': 'tag1,',
            'text': 'some text'
        }
        form = CreateQuestionForm(data=form_data)
        self.assertFalse(form.is_valid())


class QueryFormTest(TestCase):
    def test_query_param_length(self):
        random_string = ''.join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(300)
        )
        form = QueryForm(data={'q': random_string})
        self.assertFalse(form.is_valid())

