from django.db import models
from django.contrib.auth import get_user_model
from .base import BaseProjects
from common.models.base import BaseModel

# Create your models here.
class Project(BaseProjects):
    description = models.TextField(blank=True)
    prefix = models.CharField(max_length=10, unique=True)
    def save(self, *args, **kwargs):
        if not self.prefix:
            base_prefix = ''.join([w[0].upper() for w in self.name.split() if w])
            if len(base_prefix) == 1:
                base_prefix += 'P'
            elif len(base_prefix) > 10:
                base_prefix = base_prefix[:5]
            prefix = base_prefix
            counter = 1
            while Project.objects.filter(prefix=prefix).exclude(pk=self.pk).exists():
                prefix = f"{base_prefix}{counter}"
                counter += 1
            self.prefix = prefix
        super().save(*args, **kwargs)

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
