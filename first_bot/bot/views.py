from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from . import models
from .serializers import DialogSerializer


def index(request):
    return render(request, 'bot/index.html')


class DialogListView(generics.ListAPIView):
    queryset = models.Dialog.objects.all()
    serializer_class = DialogSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('parent', 'id')
