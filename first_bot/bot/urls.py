from django.urls import path, re_path
from . import views
from .views import DialogListView, DialogListViewVue
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', views.index, name='index'),
    path('api/dialogs/', DialogListView.as_view()),
    path('api/dialogs_for_vue/<int:parent_id>/', DialogListViewVue.as_view()),
    path('vue', views.vue, name='vue'),
    path('snb/', views.snb, name='snb'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # path('api/', views.api, name='api'),
    # path('api/lists/', views.lists, name='lists'),
    # path('api/questions/', views.view_list_id, name='view_list_id'),
    # path('api/questions/?list=<int:list_id>&answer=<int:question_id>', views.list_question, name='list_question'),
]
