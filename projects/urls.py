from django.urls import path # type: ignore
from .views import *

app_name = 'projects'

urlpatterns = [
    # project urls
    path('', projects_create, name='projects_create'),
    path('detail/<uuid:pk>', projects_detail, name='projects_detail'),
    path('delete/<uuid:id>', projects_delete, name='projects_delete'),
    path('projects-management/<uuid:projectId>', projects_management, name='projects_management'),
    path('api/assignments/<uuid:project_id>/', project_assignments_api, name='assignments_api'),
    # sprint urls
    path('seven-days', seven_days_create, name='seven_days_create'),
    path('seven-days/list/<uuid:project_id>/', seven_days_list, name='seven_days_list'),
    path('seven-days/edit/<uuid:pk>/', seven_days_update, name='seven_days_edit'),
    path('seven-days/delete/<uuid:pk>/', seven_days_delete, name='seven_days_delete'),
]
