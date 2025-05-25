from django.db import models
from django.contrib.auth.models import User
from common.models.base import BaseModel
from projects.models import Sprint
from .base import BaseTasks

class Epic(BaseTasks):
    sprint = models.ForeignKey(Sprint, on_delete=models.DO_NOTHING)

class Task(BaseTasks):
    sprint = models.ForeignKey(Sprint, on_delete=models.DO_NOTHING)
    epic = models.ForeignKey(Epic, on_delete=models.DO_NOTHING, related_name='tasks', null=True)

class SubTask(BaseTasks):
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING, related_name='subtasks')
    
class EpicAssignment(BaseModel):
    epic = models.ForeignKey(Epic, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='assigned_epics')

    class Meta:
        unique_together = ('epic', 'user')

class TaskAssignment(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='assigned_tasks')

    class Meta:
        unique_together = ('task', 'user')
        
class SubTaskAssignment(BaseModel):
    subtask = models.ForeignKey(SubTask, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='assigned_subtasks')

    class Meta:
        unique_together = ('subtask', 'user')

class ActivityHistory(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING, blank=True, null=True)
    epic = models.ForeignKey(Epic, on_delete=models.DO_NOTHING, blank=True, null=True)
    subtask = models.ForeignKey(SubTask, on_delete=models.DO_NOTHING, blank=True, null=True)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    