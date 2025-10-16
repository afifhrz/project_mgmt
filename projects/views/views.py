from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.urls import reverse  # type: ignore
from django.contrib.auth.models import Group, User


from projects.models.enums import SprintType
from tasks.models.enums import Status
from tasks.models.models import Task
from ..models import Project, ProjectAssignment
from common.utils.model_utils import add_json_to_model
from .thirty_days import *
from .seven_days import *


@login_required
def home(request):
    user_groups = request.user.groups.all().values_list('name', flat=True)
    if "General Manager" in user_groups or "Asset Planner" in user_groups:
        projects = Project.objects.all().order_by('-created_at')
        return render(request, 'home.html', {
            'projects': projects
        })
    if "Section Planner" in user_groups:
        tasks = Task.objects.filter(taskassignment__user=request.user).select_related(
            'sprint__project').order_by('-created_at')
        tasks = add_json_to_model(tasks)

        return render(request, 'home.html', {
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

        project = get_object_or_404(
            Project, id=project_id, created_by=request.user)
        user = get_object_or_404(User, id=user_id)

        if action == "assign":
            _, created = ProjectAssignment.objects.get_or_create(
                project=project, user=user, created_by=request.user)
            return JsonResponse({"status": "assigned" if created else "already_assigned"})
        elif action == "unassign":
            ProjectAssignment.objects.filter(
                project=project, user=user).delete()
            return JsonResponse({"status": "unassigned"})

    return render(request, "projects/projects_management.html", {
        "project": project,
        "users": users,
    })


@permission_required('projects.change_projectassignment', raise_exception=True)
def project_assignments_api(request, project_id):
    project = get_object_or_404(
        Project, id=project_id, created_by=request.user)
    assignments = ProjectAssignment.objects.filter(
        project=project).select_related('user')

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


def sprints_create(request):
    sprint_type = request.GET.get('type')
    if sprint_type not in SprintType.choices():
        return HttpResponseBadRequest("Invalid sprint type.")
    if sprint_type == SprintType.THIRTYDAYS:
        return thirty_days_create(request)
    elif sprint_type == SprintType.SEVENDAYS:
        return seven_days_create(request)


def sprints_list(request, project_id):
    sprint_type = request.GET.get('type')
    if sprint_type not in SprintType.choices():
        return HttpResponseBadRequest("Invalid sprint type.")
    if sprint_type == SprintType.THIRTYDAYS:
        return thirty_days_list(request, project_id)
    elif sprint_type == SprintType.SEVENDAYS:
        return seven_days_list(request, project_id)


def sprints_edit(request, pk):
    sprint_type = request.GET.get('type')
    if sprint_type not in SprintType.choices():
        return HttpResponseBadRequest("Invalid sprint type.")
    if sprint_type == SprintType.THIRTYDAYS:
        return thirty_days_update(request, pk)
    elif sprint_type == SprintType.SEVENDAYS:
        return seven_days_update(request, pk)


def sprints_delete(request, pk):
    sprint_type = request.GET.get('type')
    if sprint_type not in SprintType.choices():
        return HttpResponseBadRequest("Invalid sprint type.")
    if sprint_type == SprintType.THIRTYDAYS:
        return thirty_days_delete(request, pk)
    elif sprint_type == SprintType.SEVENDAYS:
        return seven_days_delete(request, pk)
