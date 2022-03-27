from django.shortcuts import render, get_object_or_404

# Create your views here.
# from django.http import HttpResponse
# from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
# from django_filters.rest_framework import DjangoFilterBackend

from . import models
from .serializers import DialogSerializer
from .models import Dialog


def index(request):
    # return HttpResponse("Хуй!")
    return render(request, 'bot/index.html')


class DialogView(APIView):
    def get(self, request):
        list_id = request.GET.get("list", "")
        if list_id and list_id != "home":
            # dialog = Dialog.objects.get(id=list_id)
            dialog = Dialog.objects.all().filter(id=list_id)
            serializer = DialogSerializer(dialog, many=True)
            child = Dialog.objects.all().filter(parent=list_id)
            child_serializer = DialogSerializer(child, many=True)
            return Response({"dialog": serializer.data, "child": child_serializer.data})
        elif list_id == "home":
            child = Dialog.objects.all().filter(parent=None)
            child_serializer = DialogSerializer(child, many=True)
            return Response({"child": child_serializer.data})
        else:
            dialog = Dialog.objects.all()
            serializer = DialogSerializer(dialog, many=True)
            return Response({"dialog": serializer.data})


# class DialogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Dialog
#         fields = '__all__'
#
#
# class DialogListView(generics.ListCreateAPIView):
#     queryset = models.Dialog.objects.all()
#     serializer_class = DialogSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_fields = ('parent',)


# def api(request):
#     return render(request, 'bot/api.html')
#
#
# def lists(request):
#     return render(request, 'bot/lists.html')
#
#
# def view_list_id(request):
#     list_id = request.GET.get("list", 1)
#     list_id = get_object_or_404(Dialog, pk=list_id)
#     return render(request, 'bot/view_list_id.html', {'list_id': list_id})
#     # return render(request, 'bot/view_list_id.html')


# def list_question(request, list_id, question_id):
#     return render(request, 'bot/list_question.html')
