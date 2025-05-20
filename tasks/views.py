from decimal import Decimal
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from common.helper.parser import _to_bool, parse_date, parse_decimal, parse_int
from common.utils.json_response import ApiResponse

from django.contrib.auth.models import User

from datetime import datetime as dt
from tasks.models.enums import RMU, PtwBasedOnRiskLevel, RiskLevel, Section, Status
from .models.models import Sprint, Epic, Task, TaskAssignment

import json

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
    task_dicts = []
    for task in tasks:
        task_dict = model_to_dict(task)
        task_dict['id'] = task.id  # Manually add the 'id' field
        task_dict['json'] = json.dumps(model_to_dict(task), indent=4, sort_keys=True, default=str)  # Convert to JSON string
        task_dicts.append(task_dict)
    # Filter users assigned to this sprint's project
    pics = User.objects.filter(assigned_projects__project=sprint.project).distinct()
    return render(request, 'tasks/tasks_list.html', {
        'sprint': sprint,
        'tasks': task_dicts,
        'pics': pics,
        "rmu_choices": RMU.choices,
        "section_choices": Section.choices,
        "risk_level_choices": RiskLevel.choices,
        "ptw_choices": PtwBasedOnRiskLevel.choices,
        "status_choices": Status.choices,
    })

@require_POST
def tasks_create(request):
    data = request.POST

    # ── 1. Required ids ───────────────────────────────────────────────
    sprint_id = data.get("sprint_id")
    pic_ids = request.POST.getlist('pic_ids')
    
    # ── 2. Basic required text fields ────────────────────────────────
    taskname = data.get("taskname")
    status   = data.get("status")
    sprint = get_object_or_404(Sprint, pk=sprint_id) if sprint_id else None
    
    if not all([sprint, taskname, status, pic_ids]):
        return JsonResponse(
            {"error": "Missing required fields."},
            status=400
        )

    # ── 3. Build the Task kwargs dict ────────────────────────────────
    task_kwargs = dict(
        sprint=sprint,
        # basic
        rmu              = data.get("rmu"),
        taskname         = taskname,
        section          = data.get("section"),
        status           = status,
        # planning
        plan_start_date  = parse_date("plan_start_date", data),
        plan_end_date    = parse_date("plan_end_date", data),
        planned_work_duration = parse_int("planned_work_duration", data),
        planned_manpower      = parse_int("planned_manpower", data),
        location         = data.get("location", ""),
        # flags
        break_in         = _to_bool(data.get("break_in")),
        need_contingency = _to_bool(data.get("need_contingency")),
        work_pack_readiness = _to_bool(data.get("work_pack_readiness", "on")),
        # risk
        risk_likelihood  = parse_int("risk_likelihood", data),
        risk_impact      = parse_int("risk_impact", data),
        ptw_based_on_risk_level = data.get("ptw_based_on_risk_level"),
        # priority
        priority_urgency = parse_int("priority_urgency", data),
        priority_impact  = parse_int("priority_impact", data),
        # budget
        budgetary_planning = parse_decimal("budgetary_planning", data),
        budgetary_actual   = parse_decimal("budgetary_actual", data),
        # misc
        remarks          = data.get("remarks", ""),
        unattained_reason= data.get("unattained_reason") or None,
    )

    # basic validation example
    if task_kwargs["plan_start_date"] is None or task_kwargs["plan_end_date"] is None:
        return ApiResponse.error(message="Invalid plan start/end date.", error={"fields":["plan_start_date","plan_end_date"]}, status=400)

    # ── 4. Persist and respond ───────────────────────────────────────
    task = Task.objects.create(**task_kwargs)
    for pic_id in pic_ids:
        user = get_object_or_404(User, pk=pic_id)
        TaskAssignment.objects.create(task=task, user=user)
    return ApiResponse.ok(message ="Task created successfully!", status=201)

@require_POST
def tasks_update(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    user = request.user

    is_planner = user.groups.filter(name="project_planner").exists()
    is_pic = task.taskassignment_set.filter(user=user).exists()

    if not (is_planner or is_pic):
        return ApiResponse.error(message="Forbidden", status=403)

    allowed = ["status", "unattained_reason"] if not is_planner else request.POST.keys()

    for field in allowed:
        if field in request.POST:
            setattr(task, field, request.POST[field] or None)

    task.save()
    return ApiResponse.ok(message="Updated")

def task_delete(pk):
    task = get_object_or_404(Task, pk=pk)
    sprint_id = task.sprint.id
    task.delete()
    return redirect('task_list', sprint_id=sprint_id)