from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.urls import reverse # type: ignore
from django.contrib.auth.models import Group, User

from projects.models import SevenDays
from tasks.models.enums import Status
from tasks.models.models import Task
from .models import Project, ProjectAssignment
from common.utils.model_utils import add_json_to_model

@login_required
def home(request):
    projects = Project.objects.all().order_by('-created_at')
    tasks = Task.objects.filter(taskassignment__user=request.user).select_related('seven_days__project').order_by('-created_at')
    tasks = add_json_to_model(tasks)
    
    return render(request, 'home.html', {
        'projects': projects, 
        'tasks': tasks,
        "status_choices": Status.choices,
        })
@permission_required('projects.view_projectassignment', raise_exception=True)
def projects_management(request, projectId):
    project = get_object_or_404(Project, id=projectId, created_by=request.user)
    pic_group = Group.objects.get(name="Section Planner")
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
        "project": project,
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
@permission_required('projects.add_sevendays', raise_exception=True)
def seven_days_create(request):
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

        overlapping = SevenDays.objects.filter(
            project=project,
            start_date__lte=end_date,
            end_date__gte=start_date,
        ).exists()

        if overlapping:
            return JsonResponse({"status": "error", "message": "Seven Days dates overlap with an existing seven days."}, status=400)

        # Save new seven_day
        SevenDays.objects.create(
            project=project,
            name=name,
            start_date=start_date,
            end_date=end_date,
            created_by=request.user,
        )

        return JsonResponse({"status": "success"})
    
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)
@permission_required('projects.view_sevendays', raise_exception=True)
def seven_days_list(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    seven_days = SevenDays.objects.filter(project=project).order_by('-start_date')
    return render(request, 'seven_days/seven_days_list.html', {'seven_days': seven_days, 'project': project})
@permission_required('projects.change_sevendays', raise_exception=True)
def seven_days_update(request, pk):
    seven_day = get_object_or_404(SevenDays, pk=pk)

    if request.method == "POST":
        name = request.POST.get("name")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        if not name or not start_date or not end_date:
            return HttpResponseBadRequest("All fields are required.")

        seven_day.name = name
        seven_day.start_date = start_date
        seven_day.end_date = end_date
        seven_day.save(user=request.user)
        messages.success(request, "7D updated successfully!")
        return HttpResponseRedirect(reverse('projects:seven_days_list', kwargs={'project_id': seven_day.project.id}))

    return render(request, "seven_days/seven_days_update.html", {"seven_day": seven_day})
@permission_required('projects.delete_sevendays', raise_exception=True)
def seven_days_delete(request, pk):
    seven_day = get_object_or_404(SevenDays, pk=pk)

    if request.method == 'POST':
        seven_day.delete()
        messages.success(request, "7D deleted successfully!")
        return HttpResponseRedirect(reverse('projects:seven_days_list', kwargs={'project_id': seven_day.project.id}))

    return render(request, 'seven_days/seven_days_delete.html', {'seven_day': seven_day})
@permission_required('projects.view_sevendays', raise_exception=True)
def seven_day_detail(request, seven_day_id):
    seven_day = get_object_or_404(SevenDays, id=seven_day_id)
    tasks = Task.objects.filter(thirty_days__seven_day=seven_day)

    tasks_by_status = {
        'OPEN': tasks.filter(status='OPEN'),
        'PROGRESS': tasks.filter(status='PROGRESS'),
        'PENDING': tasks.filter(status='PENDING'),
        'DONE': tasks.filter(status='DONE'),
    }

    return render(request, 'seven_days/seven_day_detail.html', {
        'seven_day': seven_day,
        'tasks_by_status': tasks_by_status,
    })