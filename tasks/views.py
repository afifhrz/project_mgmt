from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render, redirect

from .forms import TaskForm
from .models import Task

@require_POST
def update_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    new_status = request.POST.get('status')

    if new_status == 'PENDING' and not task.pending_reason:
        # Show modal to input pending reason (you can extend this)
        pass

    task.status = new_status
    task.save()

    return render(request, 'tasks/partials/task_card.html', {'task': task})



def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.status = 'OPEN'  # default
            task.save()
            return redirect('sprint_detail', sprint_id=task.epic.sprint.id)  # after saving, go to sprint
    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html', {'form': form})
