from django.urls import path
from .views import *

app_name = 'tasks'

urlpatterns = [
    path('tasks/', tasks_create, name='tasks_create'),
    path('<uuid:sprint_id>/tasks-list', tasks_list, name="tasks_list"),
    path('<uuid:task_id>/tasks_update', tasks_update, name="tasks_update")
]
