from django.urls import path
from .views import *

app_name = 'tasks'

urlpatterns = [
    path('tasks/', tasks_create, name='tasks_create'),
    path('<int:sprint_id>/tasks-list', tasks_list, name="tasks_list")
]
