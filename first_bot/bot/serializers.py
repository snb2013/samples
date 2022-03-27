from rest_framework import serializers

# from .models import Dialog


class DialogSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    parent_id = serializers.IntegerField()
    choice_text = serializers.CharField()
    answer_text = serializers.CharField()


