from django.db import models
from django.contrib.auth import get_user_model
from .base import BaseProjects
from common.models.base import BaseModel

# Create your models here.
class Project(BaseProjects):
    description = models.TextField(blank=True)

class Sprint(BaseProjects):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
            return f"{self.name} ({self.start_date} - {self.end_date})"

class ProjectAssignment(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, related_name='assignments')
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name='assigned_projects')

    class Meta:
        unique_together = ('project', 'user')
