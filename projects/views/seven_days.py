from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.urls import reverse
from datetime import datetime

from common.helper.url import reverse_with_query_string
from projects.models import SevenDays, Project
from projects.models.enums import SprintType

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
    seven_days = SevenDays.objects.filter(
        project=project).order_by('-start_date')
    return render(request, 'sprints/sprints_list.html', {'type':SprintType.SEVENDAYS, 'sprints': seven_days, 'project': project})


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
        return HttpResponseRedirect(reverse_with_query_string(
            'projects:sprints_list',
            params={'project_id': seven_day.project.id},
            query_params={'type': SprintType.SEVENDAYS}
        ))

    return render(request, "sprints/sprints_update.html", {"type":SprintType.SEVENDAYS, "sprint": seven_day})


@permission_required('projects.delete_sevendays', raise_exception=True)
def seven_days_delete(request, pk):
    seven_day = get_object_or_404(SevenDays, pk=pk)

    if request.method == 'POST':
        seven_day.delete()
        messages.success(request, "7D deleted successfully!")
        return HttpResponseRedirect(reverse_with_query_string(
            'projects:sprints_list',
            params={'project_id': seven_day.project.id},
            query_params={'type': SprintType.SEVENDAYS}
        ))

    return render(request, 'sprints/sprints_delete.html', {'type':SprintType.SEVENDAYS, 'sprint': seven_day})