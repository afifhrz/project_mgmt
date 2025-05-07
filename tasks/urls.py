from django.urls import path
from .views import *

app_name = 'tasks'

urlpatterns = [
    path('create/', task_create, name='create_task'),
]
