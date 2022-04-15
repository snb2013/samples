from rest_framework import viewsets
from rest_framework.response import Response

from chatbot.models import QuestionList, Question
from chatbot.serializers import QuestionListSerializer, QuestionListDetailSerializer


class QuestionListViewSet(viewsets.ModelViewSet):
    queryset = QuestionList.objects.all()
    serializer_class = QuestionListSerializer
    serializer_detail_class = QuestionListDetailSerializer
    http_method_names = ['get']


class QuestionViewSet(viewsets.ViewSet):
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        params = request.query_params
        question_list = params.get('list')
        parent_answer = params.get('answer')
        questions = Question.objects.filter(parent_answer__id=parent_answer,
                                            list_id=question_list)
        if len(questions) > 1:
            raise ValueError('Single question should be given for each answer')
        if len(questions) == 0:
            raise ValueError('Bad answer')
        question = questions[0]
        answers = [{'id': obj.id, 'text': obj.text}
                   for obj in question.answers.all()]
        result = {'text': questions[0].text, 'answers': answers}
        return Response(result)
