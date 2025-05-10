from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string # type: ignore
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy # type: ignore

from django.utils.html import escape
from django.views.generic import DetailView, ListView, UpdateView, DeleteView

from utils.alert import getErrorAlertScript, getSuccessAlertScript # type: ignore

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
    project = get_object_or_404(Project, id=request.POST["project_id"])

    if request.method == 'POST':
        form = SprintForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            name = form.cleaned_data['name']

            # Check for overlapping sprints
            overlapping = Sprint.objects.filter(
                project=project,
                start_date__lte=end,
                end_date__gte=start,
            ).exists()

            if overlapping:
                message = escape("Sprint dates overlap with an existing sprint.")
                return HttpResponse(f"{getErrorAlertScript(message)}", content_type="text/html")

            # Save new sprint if no overlap
            Sprint.objects.create(
                project=project,
                name=name,
                start_date=start,
                end_date=end,
                created_by=request.user,
            )

            message = escape("Sprint created successfully!")
            redirect_url = reverse_lazy('projects:sprint_list', kwargs={'project_id': project.id})

            return HttpResponse(f"{getSuccessAlertScript(message, redirect_url)}", content_type="text/html")

        # Invalid form
        message = escape("Invalid form submission.")
        return HttpResponse(f"{getErrorAlertScript(message)}", content_type="text/html")

    html = render_to_string("components/error.html", {"message": "Invalid request method."})
    return HttpResponse(html)

class SprintListView(ListView):
    model = Sprint
    template_name = 'sprints/sprint_list.html'
    context_object_name = 'sprints'

    def get_queryset(self):
        self.project = Project.objects.get(pk=self.kwargs['project_id'])
        return Sprint.objects.filter(project=self.project).order_by('-start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context

class SprintUpdateView(UpdateView):
    model = Sprint
    form_class = SprintForm
    template_name = 'sprints/sprint_form.html'
    
    def form_valid(self, form):
        form.save()
        return HttpResponse(status=204)  # Triggers modal close

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

@user_is_gm_or_agm
def sprint_delete_view(request, pk):
    sprint = get_object_or_404(Sprint, pk=pk)

    if request.method == "POST":
        project_id = sprint.project.id
        sprint.delete()
        success_url = reverse('projects:sprint_list', kwargs={'project_id': project_id})

        # If the request is from HTMX, return an alert and the redirect
        if request.headers.get('HX-Request'):
            message = "Sprint deleted successfully!"
            alert_html = f"""
            <div class="alert alert-success" role="alert">
                {message}
            </div>
            <script>
                $.notify('{message}', 'success');
                setTimeout(() => {{
                    window.location.href = '{success_url}';
                }}, 2000);
            </script>
            """
            response = HttpResponse(alert_html, content_type="text/html")
            response['HX-Redirect'] = success_url
            return response

        return redirect(success_url)

    return render(request, 'sprints/sprint_confirm_delete.html', {'object': sprint})

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
