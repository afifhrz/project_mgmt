from django.db import models
from django.contrib.auth.models import User
from common.models.base import BaseModel
from projects.models import ThirtyDays, SevenDays
from .base import BaseTasks


class ThirtyDaysTask(BaseTasks):
    thirty_days = models.ForeignKey(ThirtyDays, on_delete=models.CASCADE)


class Task(BaseTasks):
    thirty_days_task = models.ForeignKey(ThirtyDaysTask, on_delete=models.CASCADE, related_name='seven_days_tasks', null=True)
    seven_days = models.ForeignKey(SevenDays, on_delete=models.CASCADE)


class ThirtyDaysTaskAssignment(BaseModel):
    thirty_days_task = models.ForeignKey(ThirtyDaysTask, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_thirty_days')

    class Meta:
        unique_together = ('thirty_days_task', 'user')


class TaskAssignment(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')

    class Meta:
        unique_together = ('task', 'user')


class ActivityHistory(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)
    thirty_days_task = models.ForeignKey(ThirtyDaysTask, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
