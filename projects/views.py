from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView # type: ignore
from .decorators import user_is_gm_or_agm
from projects.models import Sprint
from tasks.models import Task
from .forms import ProjectForm, SprintForm
from .models import Project

@login_required
def home(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'projects': projects})

@user_is_gm_or_agm
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user  # assume user is logged in
            project.save()
            return redirect('home')  # go back to home after create
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form})

@user_is_gm_or_agm
def project_delete(request, id):
    project = get_object_or_404(Project, id=id)
    project.delete()
    return redirect('home')

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'  # This will link to the above template
    context_object_name = 'project'  # This makes 'project' available in the template

@user_is_gm_or_agm
def sprint_create(request):
    if request.method == 'POST':
        form = SprintForm(request.POST)
        if form.is_valid():
            sprint = form.save(commit=False)
            sprint.project = get_object_or_404(Project, id=request.POST.get('project_id'))
            sprint.created_by = request.user  # assume user is logged in
            sprint.save()
            return redirect('home')  # go back to home after create
    else:
        form = SprintForm()
    return render(request, 'projects/sprint_form.html', {'form': form})

def sprint_detail(request, sprint_id):
    sprint = get_object_or_404(Sprint, id=sprint_id)
    tasks = Task.objects.filter(epic__sprint=sprint)

    tasks_by_status = {
        'OPEN': tasks.filter(status='OPEN'),
        'PROGRESS': tasks.filter(status='PROGRESS'),
        'PENDING': tasks.filter(status='PENDING'),
        'DONE': tasks.filter(status='DONE'),
    }

    return render(request, 'sprints/sprint_detail.html', {
        'sprint': sprint,
        'tasks_by_status': tasks_by_status,
    })
