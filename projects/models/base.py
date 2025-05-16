from common.models.base import BaseModel
from django.db import models

class BaseProjects(BaseModel):
    name = models.CharField(max_length=255)
    
    class Meta:
        abstract = True