from django import forms
from .models import Epic, Task, SubTask

class EpicForm(forms.ModelForm):
    class Meta:
        model = Epic
        fields = ['title', 'description']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['epic', 'assigned_to', 'title', 'description', 'status', 'pending_reason']

class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ['title', 'description', 'status', 'pending_reason']
