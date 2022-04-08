from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from . import models
from .serializers import DialogSerializer


def index(request):
    return render(request, 'bot/index.html')


def vue(request):
    return render(request, 'bot/vue.html')


class DialogListView(generics.ListAPIView):
    queryset = models.Dialog.objects.all()
    serializer_class = DialogSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('parent', 'id')


class DialogListViewVue(generics.ListAPIView):
    serializer_class = DialogSerializer

    def get_queryset(self):
        parent_id = self.kwargs['parent_id']
        if parent_id != 0:
            return models.Dialog.objects.filter(parent=parent_id)
        else:
            return models.Dialog.objects.filter(parent=None)

# class DialogListViewVue(generics.RetrieveAPIView):
#     queryset = models.Dialog.objects.all()
#     serializer_class = DialogSerializer
