from django.urls import path # type: ignore
from .views import *

app_name = 'projects'

urlpatterns = [
    # home page
    path('', home, name='projects_list'),
    # project urls
    path('projects', projects_create, name='projects_create'),
    path('projects-detail/<int:pk>', projects_detail, name='projects_detail'),
    path('projects-delete/<int:id>', projects_delete, name='projects_delete'),
    # sprint urls
    path('sprints', sprints_create, name='sprints_create'),
    path('<int:project_id>/sprints-list/', sprints_list, name='sprints_list'),
    path('sprints/<int:pk>/sprints-edit/', sprints_update, name='sprints_edit'),
    path('sprints/<int:pk>/sprints-delete/', sprints_delete, name='sprints_delete'),
]
