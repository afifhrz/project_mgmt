from django.urls import path # type: ignore
from .views import *

app_name = 'projects'

urlpatterns = [
    # home page
    path('', home, name='projects_list'),
    path('', home, name='home'),
    # project urls
    path('projects', projects_create, name='projects_create'),
    path('projects-detail/<uuid:pk>', projects_detail, name='projects_detail'),
    path('projects-delete/<uuid:id>', projects_delete, name='projects_delete'),
    path('projects_management', projects_management, name='projects_management'),
    path('api/assignments/<uuid:project_id>/', project_assignments_api, name='assignments_api'),
    # sprint urls
    path('sprints', sprints_create, name='sprints_create'),
    path('<uuid:project_id>/sprints-list/', sprints_list, name='sprints_list'),
    path('sprints/<uuid:pk>/sprints-edit/', sprints_update, name='sprints_edit'),
    path('sprints/<uuid:pk>/sprints-delete/', sprints_delete, name='sprints_delete'),
]
