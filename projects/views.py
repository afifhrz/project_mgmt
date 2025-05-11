from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy # type: ignore

from django.utils.html import escape
from .decorators import user_is_gm_or_agm
from projects.models import Sprint
from tasks.models import Task
from .models import Project

@login_required
def home(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'projects': projects})

@user_is_gm_or_agm
def projects_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")

        if not name:
            return JsonResponse({"error": "Project name is required."}, status=400)

        project = Project.objects.create(
            name=name,
            description=description,
            created_by=request.user,
        )

        return JsonResponse({"message": "Project created successfully.", "project_id": project.id})

    return HttpResponseBadRequest("Invalid request method.")

@user_is_gm_or_agm
def projects_delete(request, id):
    project = get_object_or_404(Project, id=id)
    project.delete()
    return redirect('home')

@user_is_gm_or_agm
def projects_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/projects_detail.html', {'project': project})

@user_is_gm_or_agm
def sprints_create(request):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=request.POST["project_id"])
        name = request.POST.get('name', '').strip()
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')

        if not name or not start or not end:
            return JsonResponse({"status": "error", "message": "All fields are required."}, status=400)

        # Convert dates
        try:
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
        except ValueError:
            return JsonResponse({"status": "error", "message": "Invalid date format."}, status=400)

        if start_date > end_date:
            return JsonResponse({"status": "error", "message": "Start date cannot be after end date."}, status=400)

        overlapping = Sprint.objects.filter(
            project=project,
            start_date__lte=end_date,
            end_date__gte=start_date,
        ).exists()

        if overlapping:
            return JsonResponse({"status": "error", "message": "Sprint dates overlap with an existing sprint."}, status=400)

        # Save new sprint
        Sprint.objects.create(
            project=project,
            name=name,
            start_date=start_date,
            end_date=end_date,
            created_by=request.user,
        )

        return JsonResponse({"status": "success"})
    
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)


@user_is_gm_or_agm
def sprints_list(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    sprints = Sprint.objects.filter(project=project).order_by('-start_date')
    return render(request, 'sprints/sprints_list.html', {'sprints': sprints, 'project': project})

@user_is_gm_or_agm
def sprints_update(request, pk):
    sprint = get_object_or_404(Sprint, pk=pk)

    if request.method == "POST":
        name = request.POST.get("name")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        if not name or not start_date or not end_date:
            return HttpResponseBadRequest("All fields are required.")

        sprint.name = name
        sprint.start_date = start_date
        sprint.end_date = end_date
        sprint.save()
        messages.success(request, "Sprint updated successfully!")
        return HttpResponseRedirect(reverse('projects:sprints_list', kwargs={'project_id': sprint.project.id}))

    return render(request, "sprints/sprints_update.html", {"sprint": sprint})

@user_is_gm_or_agm
def sprints_delete(request, pk):
    print("ok")
    sprint = get_object_or_404(Sprint, pk=pk)

    if request.method == 'POST':
        sprint.delete()
        messages.success(request, "Sprint deleted successfully!")
        return HttpResponseRedirect(reverse('projects:sprints_list', kwargs={'project_id': sprint.project.id}))

    return render(request, 'sprints/sprints_delete.html', {'sprint': sprint})

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

# Task
@user_is_gm_or_agm
def tasks_list(request, sprint_id):
    sprint = get_object_or_404(Sprint, id=sprint_id)
    tasks = Task.objects.filter(epic__sprint=sprint)

    tasks_by_status = {
        'OPEN': tasks.filter(status='OPEN'),
        'PROGRESS': tasks.filter(status='PROGRESS'),
        'PENDING': tasks.filter(status='PENDING'),
        'DONE': tasks.filter(status='DONE'),
    }

    return render(request, 'tasks/tasks_list.html', {
        'tasks': tasks,
        'tasks_by_status': tasks_by_status,
    })