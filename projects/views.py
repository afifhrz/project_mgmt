from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.urls import reverse # type: ignore
from django.contrib.auth.models import Group, User

from projects.models import Sprint
from tasks.models.enums import Status
from tasks.models.models import Task
from .models import Project, ProjectAssignment
from common.utils.model_utils import add_json_to_model

@login_required
def home(request):
    projects = Project.objects.all().order_by('-created_at')
    tasks = Task.objects.filter(taskassignment__user=request.user).select_related('sprint__project').order_by('-created_at')
    tasks = add_json_to_model(tasks)
    
    return render(request, 'home.html', {
        'projects': projects, 
        'tasks': tasks,
        "status_choices": Status.choices,
        })
@permission_required('projects.view_projectassignment', raise_exception=True)
def projects_management(request):
    projects = Project.objects.filter(created_by=request.user)
    pic_group = Group.objects.get(name="Person In Charge")
    users = pic_group.user_set.all()

    if request.method == "POST":
        action = request.POST.get("action")
        project_id = request.POST.get("project_id")
        user_id = request.POST.get("user_id")

        project = get_object_or_404(Project, id=project_id, created_by=request.user)
        user = get_object_or_404(User, id=user_id)

        if action == "assign":
            _, created = ProjectAssignment.objects.get_or_create(project=project, user=user, created_by=request.user)
            return JsonResponse({"status": "assigned" if created else "already_assigned"})
        elif action == "unassign":
            ProjectAssignment.objects.filter(project=project, user=user).delete()
            return JsonResponse({"status": "unassigned"})

    return render(request, "projects/projects_management.html", {
        "projects": projects,
        "users": users,
    })
@permission_required('projects.change_projectassignment', raise_exception=True)
def project_assignments_api(request, project_id):
    project = get_object_or_404(Project, id=project_id, created_by=request.user)
    assignments = ProjectAssignment.objects.filter(project=project).select_related('user')

    data = [
        {
            "id": assignment.user.id,
            "name": assignment.user.get_full_name(),
            "email": assignment.user.email,
        }
        for assignment in assignments
    ]
    return JsonResponse(data, safe=False)
@permission_required('projects.add_project', raise_exception=True)
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
@permission_required('projects.delete_project', raise_exception=True)
def projects_delete(request, id):
    project = get_object_or_404(Project, id=id)
    project.delete()
    return redirect('home')
@permission_required('projects.view_project', raise_exception=True)
def projects_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/projects_detail.html', {'project': project})
@permission_required('projects.add_sprint', raise_exception=True)
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
@permission_required('projects.view_sprint', raise_exception=True)
def sprints_list(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    sprints = Sprint.objects.filter(project=project).order_by('-start_date')
    return render(request, 'sprints/sprints_list.html', {'sprints': sprints, 'project': project})
@permission_required('projects.change_sprint', raise_exception=True)
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
        sprint.save(user=request.user)
        messages.success(request, "Sprint updated successfully!")
        return HttpResponseRedirect(reverse('projects:sprints_list', kwargs={'project_id': sprint.project.id}))

    return render(request, "sprints/sprints_update.html", {"sprint": sprint})
@permission_required('projects.delete_sprint', raise_exception=True)
def sprints_delete(request, pk):
    print("ok")
    sprint = get_object_or_404(Sprint, pk=pk)

    if request.method == 'POST':
        sprint.delete()
        messages.success(request, "Sprint deleted successfully!")
        return HttpResponseRedirect(reverse('projects:sprints_list', kwargs={'project_id': sprint.project.id}))

    return render(request, 'sprints/sprints_delete.html', {'sprint': sprint})
@permission_required('projects.view_sprint', raise_exception=True)
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