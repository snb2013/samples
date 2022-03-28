from django.urls import path

from . import views
from .views import DialogListView

urlpatterns = [
    path('', views.index, name='index'),
    path('api/dialogs/', DialogListView.as_view()),

    # path('api/', views.api, name='api'),
    # path('api/lists/', views.lists, name='lists'),
    # path('api/questions/', views.view_list_id, name='view_list_id'),
    # path('api/questions/?list=<int:list_id>&answer=<int:question_id>', views.list_question, name='list_question'),
]
