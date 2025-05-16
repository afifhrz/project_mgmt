from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.models import User
from django.urls import reverse

from tasks.models.enums import Status
from .models.models import Sprint, Epic, Task

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

def tasks_list(request, sprint_id):
    sprint = get_object_or_404(Sprint, id=sprint_id)
    tasks = Task.objects.filter(sprint=sprint)
    status_choices = Status.choices
    
    # Filter users assigned to this sprint's project
    pics = User.objects.filter(assigned_projects__project=sprint.project).distinct()

    return render(request, 'tasks/tasks_list.html', {
        'sprint': sprint,
        'tasks': tasks,
        'pics': pics,
        'status_choices': status_choices
    })

def tasks_create(request):
    if request.method == 'POST':
        sprint_id = request.POST.get('sprint_id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        pic_id = request.POST.get('pic_id')

        if not all([sprint_id, title, status, pic_id]):
            return JsonResponse({'error': 'Please fill in all required fields!'}, status=400)

        sprint = get_object_or_404(Sprint, id=sprint_id)

        Task.objects.create(
            sprint=sprint,
            title=title,
            description=description,
            status=status,
            assigned_to=User.objects.filter(pk=pic_id).first()
        )

        return JsonResponse({'message': 'Task created successfully!'}, status=200)

    return JsonResponse({'error': 'Invalid method!'}, status=400)

def tasks_update_status(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.status = request.POST.get('status')
        task.save()
        return redirect('tasks:tasks_list', sprint_id=task.sprint.id)

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    sprint_id = task.sprint.id
    task.delete()
    return redirect('task_list', sprint_id=sprint_id)