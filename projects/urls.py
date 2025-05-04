from django.urls import path # type: ignore
from .views import *

app_name = 'projects'

urlpatterns = [
    path('create/', project_create, name='create'),
    path('detail/<int:pk>', ProjectDetailView.as_view(), name='detail'),
    path('delete/<int:id>', project_delete, name='delete'),
    path('sprint', start_sprint, name='start_sprint'),
    path('<int:project_id>/sprints/', SprintListView.as_view(), name='sprint_list'),
    path('sprint/<int:pk>/edit/', SprintUpdateView.as_view(), name='sprint_edit'),
    path('sprint/<int:pk>/delete/', sprint_delete_view, name='sprint_delete'),  
    path('', home, name='list'),
]
