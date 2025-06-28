from django.urls import path # type: ignore
from .views.views import *

app_name = 'projects'

urlpatterns = [
    # project urls
    path('', projects_create, name='projects_create'),
    path('detail/<uuid:pk>', projects_detail, name='projects_detail'),
    path('delete/<uuid:id>', projects_delete, name='projects_delete'),
    path('projects-management/<uuid:projectId>', projects_management, name='projects_management'),
    path('api/assignments/<uuid:project_id>/', project_assignments_api, name='assignments_api'),
    # sprint urls
    path('sprint', sprints_create, name='sprints_create'),
    path('sprint/list/<uuid:project_id>/', sprints_list, name='sprints_list'),
    path('sprint/edit/<uuid:pk>/', sprints_edit, name='sprints_edit'),
    path('sprint/delete/<uuid:pk>/', sprints_delete, name='sprints_delete'),
]
