from rest_framework import serializers

from chatbot.models import QuestionList, Question, Answer


class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionList
        fields = ('id', 'name')

class QuestionListDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionList
        fields = ('id', 'name', 'questions')

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionList
        fields = ('id', 'text')
