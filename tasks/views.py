from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from common.helper.parser import _to_bool, parse_date, parse_decimal, parse_int
from common.utils.json_response import ApiResponse
from django.utils.text import slugify

from django.contrib.auth.models import User
from django.utils.timezone import now

from projects.models import SevenDays, ThirtyDays
from projects.models.enums import SprintType
from tasks.models.enums import RMU, PtwBasedOnRiskLevel, RiskLevel, Section, Status
from .models.models import ActivityHistory, SevenDays, ThirtyDaysTask, Task, TaskAssignment
from common.utils.model_utils import add_json_to_model, prettify_field

# Tasks List View for Thirty Days


def thirty_day_tasks_list(request, thirty_day_id):
    thirty_day = get_object_or_404(ThirtyDays, id=thirty_day_id)
    thirty_day_tasks = ThirtyDaysTask.objects.filter(thirty_days=thirty_day)
    thirty_day_tasks = add_json_to_model(thirty_day_tasks)
    return render(request, 'tasks/tasks_list.html', {
        "type": "thirty_days",
        "sprint": thirty_day,
        "sprint_tasks": thirty_day_tasks,
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
    seven_day_id = data.get("seven_day_id")
    pic_ids = request.POST.getlist('pic_ids')

    # ── 2. Basic required text fields ────────────────────────────────
    taskname = data.get("taskname")
    status = data.get("status")
    seven_day = get_object_or_404(
        SevenDays, pk=seven_day_id) if seven_day_id else None

    if not all([seven_day, taskname, status, pic_ids]):
        return JsonResponse(
            {"error": "Missing required fields."},
            status=400
        )

    # ── 3. Build the Task kwargs dict ────────────────────────────────
    task_kwargs = dict(
        seven_days=seven_day,
        # basic
        rmu=data.get("rmu"),
        taskname=taskname,
        section=data.get("section"),
        status=status,
        # planning
        plan_start_date=parse_date("plan_start_date", data),
        plan_end_date=parse_date("plan_end_date", data),
        planned_work_duration=parse_int("planned_work_duration", data),
        planned_manpower=parse_int("planned_manpower", data),
        location=data.get("location", ""),
        # flags
        break_in=_to_bool(data.get("break_in")),
        need_contingency=_to_bool(data.get("need_contingency")),
        work_pack_readiness=_to_bool(data.get("work_pack_readiness", "on")),
        # risk
        risk_likelihood=parse_int("risk_likelihood", data),
        risk_impact=parse_int("risk_impact", data),
        ptw_based_on_risk_level=data.get("ptw_based_on_risk_level"),
        # priority
        priority_urgency=parse_int("priority_urgency", data),
        priority_impact=parse_int("priority_impact", data),
        # budget
        budgetary_planning=parse_decimal("budgetary_planning", data),
        budgetary_actual=parse_decimal("budgetary_actual", data),
        # misc
        remarks=data.get("remarks", ""),
        unattained_reason=data.get("unattained_reason") or None,
        created_by=request.user,
        updated_by=request.user,
    )

    # basic validation example
    if task_kwargs["plan_start_date"] is None or task_kwargs["plan_end_date"] is None:
        return ApiResponse.error(message="Invalid plan start/end date.", error={"fields": ["plan_start_date", "plan_end_date"]}, status=400)

    # ── 4. Persist and respond ───────────────────────────────────────
    task = Task.objects.create(**task_kwargs)
    for pic_id in pic_ids:
        user = get_object_or_404(User, pk=pic_id)
        TaskAssignment.objects.create(task=task, user=user)
    return ApiResponse.ok(message="Task created successfully!", status=201)


def tasks_delete(pk):
    task = get_object_or_404(Task, pk=pk)
    sprint_id = task.sprint.id
    task.delete()
    return redirect('task_list', sprint_id=sprint_id)


def tasks_redirect_view(request, issue_id):
    task = get_object_or_404(Task, issue_id=issue_id)
    slug = slugify(task.taskname)
    return redirect('tasks:tasks_detail', issue_id=issue_id, task_name=slug)


def tasks_detail_view(request, issue_id, task_name=None):
    task = get_object_or_404(Task, issue_id=issue_id)
    seven_days = SevenDays.objects.filter(project=task.seven_days.project)
    pics = User.objects.filter(
        assigned_projects__project=task.seven_days.project).distinct()
    assigned_user_ids = task.taskassignment_set.all().values_list('user_id', flat=True)
    return render(request, 'tasks/tasks_detail.html',
                  {
                      'task': task,
                      'status_choices': Status.choices,
                      'risk_level_choices': RiskLevel.choices,
                      'rmu_choices': RMU.choices,
                      'section_choices': Section.choices,
                      'ptw_choices': PtwBasedOnRiskLevel.choices,
                      'seven_days': seven_days,
                      'pics': pics,
                      'assigned_user_ids': assigned_user_ids,
                  })

# Tasks List View for Seven Days


def tasks_list(request, sprint_id):
    type = request.GET.get("type")
    if type not in SprintType.choices():
        return JsonResponse({"error": "Invalid sprint type."}, status=400)
    # Determine the parent task model based on the type
    parent_task = SevenDays if type == SprintType.SEVENDAYS else ThirtyDays
    task_entity = Task if type == SprintType.SEVENDAYS else ThirtyDaysTask
    
    sprint = get_object_or_404(parent_task, id=sprint_id)
    tasks = task_entity.objects.filter(sprint=sprint)
    tasks = add_json_to_model(tasks)
    # Filter users assigned to this sprint's project
    pics = User.objects.filter(
        assigned_projects__project=sprint.project).distinct()
    return render(request, 'tasks/tasks_list.html', {
        'type': type,
        'sprint': sprint,
        'tasks': tasks,
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
    seven_day_id = data.get("seven_day_id")
    pic_ids = request.POST.getlist('pic_ids')

    # ── 2. Basic required text fields ────────────────────────────────
    taskname = data.get("taskname")
    status = data.get("status")
    seven_day = get_object_or_404(
        SevenDays, pk=seven_day_id) if seven_day_id else None

    if not all([seven_day, taskname, status, pic_ids]):
        return JsonResponse(
            {"error": "Missing required fields."},
            status=400
        )

    # ── 3. Build the Task kwargs dict ────────────────────────────────
    task_kwargs = dict(
        seven_days=seven_day,
        # basic
        rmu=data.get("rmu"),
        taskname=taskname,
        section=data.get("section"),
        status=status,
        # planning
        plan_start_date=parse_date("plan_start_date", data),
        plan_end_date=parse_date("plan_end_date", data),
        planned_work_duration=parse_int("planned_work_duration", data),
        planned_manpower=parse_int("planned_manpower", data),
        location=data.get("location", ""),
        # flags
        break_in=_to_bool(data.get("break_in")),
        need_contingency=_to_bool(data.get("need_contingency")),
        work_pack_readiness=_to_bool(data.get("work_pack_readiness", "on")),
        # risk
        risk_likelihood=parse_int("risk_likelihood", data),
        risk_impact=parse_int("risk_impact", data),
        ptw_based_on_risk_level=data.get("ptw_based_on_risk_level"),
        # priority
        priority_urgency=parse_int("priority_urgency", data),
        priority_impact=parse_int("priority_impact", data),
        # budget
        budgetary_planning=parse_decimal("budgetary_planning", data),
        budgetary_actual=parse_decimal("budgetary_actual", data),
        # misc
        remarks=data.get("remarks", ""),
        unattained_reason=data.get("unattained_reason") or None,
        created_by=request.user,
        updated_by=request.user,
    )

    # basic validation example
    if task_kwargs["plan_start_date"] is None or task_kwargs["plan_end_date"] is None:
        return ApiResponse.error(message="Invalid plan start/end date.", error={"fields": ["plan_start_date", "plan_end_date"]}, status=400)

    # ── 4. Persist and respond ───────────────────────────────────────
    task = Task.objects.create(**task_kwargs)
    for pic_id in pic_ids:
        user = get_object_or_404(User, pk=pic_id)
        TaskAssignment.objects.create(task=task, user=user)
    return ApiResponse.ok(message="Task created successfully!", status=201)


def tasks_delete(pk):
    task = get_object_or_404(Task, pk=pk)
    sprint_id = task.sprint.id
    task.delete()
    return redirect('task_list', sprint_id=sprint_id)


def tasks_redirect_view(request, issue_id):
    task = get_object_or_404(Task, issue_id=issue_id)
    slug = slugify(task.taskname)
    return redirect('tasks:tasks_detail', issue_id=issue_id, task_name=slug)


def tasks_detail_view(request, issue_id, task_name=None):
    task = get_object_or_404(Task, issue_id=issue_id)
    seven_days = SevenDays.objects.filter(project=task.seven_days.project)
    pics = User.objects.filter(
        assigned_projects__project=task.seven_days.project).distinct()
    assigned_user_ids = task.taskassignment_set.all().values_list('user_id', flat=True)
    return render(request, 'tasks/tasks_detail.html',
                  {
                      'task': task,
                      'status_choices': Status.choices,
                      'risk_level_choices': RiskLevel.choices,
                      'rmu_choices': RMU.choices,
                      'section_choices': Section.choices,
                      'ptw_choices': PtwBasedOnRiskLevel.choices,
                      'seven_days': seven_days,
                      'pics': pics,
                      'assigned_user_ids': assigned_user_ids,
                  })


@csrf_exempt
def update_tasks_ajax(request):
    if request.method == "POST":
        task = get_object_or_404(Task, id=request.POST.get('task_id'))
        changes = []

        def check_and_update(field):
            old_value = getattr(task, field)
            new_value = request.POST.get(field)
            # Handle checkbox booleans
            if isinstance(old_value, bool):
                new_value = request.POST.get(field) == 'on'
            if str(old_value) != str(new_value) and new_value is not None:
                setattr(task, field, new_value)
                pretty_field = prettify_field(field)
                changes.append(
                    f"{pretty_field} changed from '{old_value}' to '{new_value}' by {request.user.get_full_name()}")

        updatable_fields = [
            'taskname', 'rmu', 'section', 'location', 'planned_work_duration', 'planned_manpower',
            'remarks', 'unattained_reason', 'risk_level', 'risk_likelihood', 'risk_impact',
            'priority_urgency', 'priority_impact', 'ptw_based_on_risk_level',
            'budgetary_planning', 'budgetary_actual', 'status'
        ]

        for field in updatable_fields:
            check_and_update(field)

        pics = request.POST.getlist('pic_ids')
        if pics:
            current_pics = set(
                task.taskassignment_set.values_list('user_id', flat=True))
            new_pics = set(map(int, pics))
            added_pics = new_pics - current_pics
            removed_pics = current_pics - new_pics

            for pic_id in added_pics:
                user = get_object_or_404(User, id=pic_id)
                TaskAssignment.objects.get_or_create(task=task, user=user)
                changes.append(
                    f"Added PIC with name: {user.first_name} {user.last_name} by {request.user.get_full_name()}")

            for pic_id in removed_pics:
                TaskAssignment.objects.filter(
                    task=task, user_id=pic_id).delete()
                user = get_object_or_404(User, id=pic_id)
                changes.append(
                    f"Removed PIC with name: {user.first_name} {user.last_name} by {request.user.get_full_name()}")

        seven_days = request.POST.get('seven_days')
        if seven_days:
            new_seven_days = get_object_or_404(SevenDays, id=seven_days)
            if task.seven_days != new_seven_days:
                changes.append(
                    f"7D changed from {task.seven_days.name} to {new_seven_days.name} by {request.user.get_full_name()}")
                task.seven_days = new_seven_days

        # Save changes and log history
        if changes:
            task.save(user=request.user)
            change_description = "; ".join(changes)
            ActivityHistory.objects.create(
                task=task, description=change_description)
            return JsonResponse({
                "success": True,
                "timestamp": now().strftime("%Y-%m-%d %H:%M"),
                "change_description": change_description,
            })

        return JsonResponse({"success": True, "message": "No changes detected."})

    return JsonResponse({"success": False}, status=400)
