import json
import unittest

from django.conf import settings
from rest_framework.test import RequestsClient

from chatbot.models import QuestionList, Question, Answer


class TestApi(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestApi, self).__init__(*args, **kwargs)
        settings.DEBUG = True

    def setUp(self):
        l, is_new = QuestionList.objects.get_or_create(name='L1', order=0)
        QuestionList.objects.get_or_create(name='L2', order=1)
        self.q1, is_new = Question.objects.get_or_create(text='Q1', list=l)
        self.a1_q1, is_new = Answer.objects.get_or_create(
            text='A1_Q1', parent_question=self.q1, order=0)
        self.a2_q1, is_new = Answer.objects.get_or_create(
            text='A2_Q1', parent_question=self.q1, order=1)
        self.q2, is_new = Question.objects.get_or_create(
            text='Q2', parent_answer=self.a1_q1, list=l)
        self.client = RequestsClient()

    def test_question_lists(self):
        response = self.client.get('http://testserver/api/lists')
        data = json.loads(response.text)
        self.assertListEqual(data,
                             [{'name': 'L1', 'id': 1},
                              {'name': 'L2', 'id': 2}])

    def test_questions(self):
        response = self.client.get('http://testserver/api/questions/?list=1')
        data = json.loads(response.text)
        self.assertDictEqual(data, {'answers': [{'id': 1, 'text': 'A1_Q1'},
                                                {'id': 2, 'text': 'A2_Q1'}],
                                    'text': 'Q1'})

        response = self.client.get(
            'http://testserver/api/questions/?list=1&answer=%s' %
            self.a1_q1.id)
        data = json.loads(response.text)
        self.assertDictEqual(data, {'answers': [], 'text': 'Q2'})
