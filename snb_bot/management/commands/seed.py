import json
import os

from django.conf import settings
from django.core.management import BaseCommand

from chatbot.models import QuestionList, Question, Answer


def seed(filename):
    """
    Fill DB with QA base
    :param filename: Source file name
    """
    def add_question(text, answers, question_list, parent_answer=None):
        q = Question(text=text, parent_answer=parent_answer,
                     list=question_list)
        q.save()
        for order, answer in enumerate(answers):
            answer_text = answer[0]
            child_question_text = answer[1]
            a = Answer(text=answer_text, parent_question=q, order=order)
            a.save()
            add_question(child_question_text,
                         answer[2] if len(answer) > 2 else [],
                         question_list, a)

    f = open(os.path.join(settings.BASE_DIR, filename))
    content = f.read()
    data = json.loads(content)

    Question.objects.all().delete()
    Answer.objects.all().delete()

    for order, row in enumerate(data):
        question_list = QuestionList(name=row[0], order=order)
        question_list.save()
        add_question(row[1], row[2], question_list)  # root question


class Command(BaseCommand):
    help = """
        Fill DB with QA base
        Arguments:
            filename: Source file name
    """

    def add_arguments(self, parser):
        parser.add_argument('filename')

    def handle(self, *args, **options):
        seed(filename=options['filename'])
