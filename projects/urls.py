from django.urls import path # type: ignore
from .views import home, project_create, ProjectDetailView, project_delete

app_name = 'projects'

urlpatterns = [
    path('create/', project_create, name='create'),
    path('detail/<int:pk>', ProjectDetailView.as_view(), name='detail'),
    path('delete/<int:id>', project_delete, name='delete'),
    path('delete/<int:id>', project_delete, name='sprint_create'),
    path('', home, name='list'),
]
