from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse

from .models import Dialog


def index(request):
    # return HttpResponse("Хуй!")
    return render(request, 'bot/index.html')


def api(request):
    return render(request, 'bot/api.html')


def lists(request):
    return render(request, 'bot/lists.html')


def view_list_id(request):
    list_id = request.GET.get("list", 1)
    list_id = get_object_or_404(Dialog, pk=list_id)
    return render(request, 'bot/view_list_id.html', {'list_id': list_id})
    # return render(request, 'bot/view_list_id.html')


def list_question(request, list_id, question_id):
    return render(request, 'bot/list_question.html')
