from django.urls import path
from .views import *

app_name = 'tasks'

urlpatterns = [
    path('', tasks_create, name='tasks_create'),
    path('list/<uuid:seven_day_id>', tasks_list, name="tasks_list"),
    path('update/', update_task_ajax, name='tasks_update_ajax'),
    path('<str:issue_id>/', tasks_redirect_view, name='tasks_redirect'),
    path('<str:issue_id>/<slug:task_name>/', tasks_detail_view, name='tasks_detail'),
]
