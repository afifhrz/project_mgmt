from django.db import models
from django.contrib.auth.models import User

from projects.models import Sprint

# Create your models here.
class Epic(models.Model):
    sprint = models.ForeignKey(Sprint, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

class Task(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('PROGRESS', 'On Progress'),
        ('PENDING', 'Pending'),
        ('DONE', 'Done'),
        ('CANCELLED', 'Cancelled'),
        ('REOPEN', 'Reopen'),
    ]
    sprint = models.ForeignKey(Sprint, on_delete=models.DO_NOTHING)
    epic = models.ForeignKey(Epic, on_delete=models.DO_NOTHING, related_name='tasks', null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')
    pending_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING, related_name='subtasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=Task.STATUS_CHOICES, default='OPEN')
    pending_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)