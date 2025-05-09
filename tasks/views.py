from django.shortcuts import render, get_object_or_404, redirect
from .models import Sprint, Epic, Task, SubTask
from .forms import EpicForm, TaskForm, SubTaskForm
from django.http import HttpResponse

# --- Epic Views ---
def epic_list(request, sprint_id):
    sprint = get_object_or_404(Sprint, id=sprint_id)
    epics = Epic.objects.filter(sprint=sprint)
    return render(request, 'epic/list.html', {'sprint': sprint, 'epics': epics})

def epic_create(request, sprint_id):
    sprint = get_object_or_404(Sprint, id=sprint_id)
    form = EpicForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        epic = form.save(commit=False)
        epic.sprint = sprint
        epic.save()
        return redirect('epic_list', sprint_id=sprint.id)
    return render(request, 'epic/form.html', {'form': form})

def epic_update(request, pk):
    epic = get_object_or_404(Epic, pk=pk)
    form = EpicForm(request.POST or None, instance=epic)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('epic_list', sprint_id=epic.sprint.id)
    return render(request, 'epic/form.html', {'form': form})

def epic_delete(request, pk):
    epic = get_object_or_404(Epic, pk=pk)
    sprint_id = epic.sprint.id
    epic.delete()
    return redirect('epic_list', sprint_id=sprint_id)

def task_list(request, sprint_id):
    sprint = get_object_or_404(Sprint, id=sprint_id)
    tasks = Task.objects.filter(sprint=sprint)
    return render(request, 'tasks/list.html', {'sprint': sprint, 'task': tasks})

def task_create(request):
    if request.method == 'POST' and form.is_valid():
        sprint = get_object_or_404(Sprint, id=request.POST.sprint_id)
        form = TaskForm(request.POST or None)
        task = form.save(commit=False)
        task.sprint = sprint
        task.save()
        return redirect('task_list', sprint_id=sprint.id)
    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html', {'form': form})

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = EpicForm(request.POST or None, instance=task)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('task_list', sprint_id=task.sprint.id)
    return render(request, 'task/form.html', {'form': form})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    sprint_id = task.sprint.id
    task.delete()
    return redirect('task_list', sprint_id=sprint_id)