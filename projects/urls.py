from django.urls import path # type: ignore
from .views import *

app_name = 'projects'

urlpatterns = [
    # home page
    path('', home, name='project_list'),
    # project urls
    path('create/', project_create, name='project_create'),
    path('detail/<int:pk>', ProjectDetailView.as_view(), name='project_detail'),
    path('delete/<int:id>', project_delete, name='project_delete'),
    # sprint urls
    path('sprint', sprint_create, name='sprint_create'),
    path('<int:project_id>/sprints/', SprintListView.as_view(), name='sprint_list'),
    path('sprint/<int:pk>/edit/', SprintUpdateView.as_view(), name='sprint_edit'),
    path('sprint/<int:pk>/delete/', sprint_delete_view, name='sprint_delete'),  
]
