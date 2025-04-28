from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from users.http import AuthenticatedHttpRequest

from .forms import ProjectForm
from .models import Project


@login_required
def project_create(request: AuthenticatedHttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.organization = request.user.organization
            project.save()
            return render(request, 'projects/partials/form_success.html')

        return render(request, 'projects/partials/form.html', {'form': form})

    form = ProjectForm()
    return render(request, 'projects/create.html', {'form': form})


@login_required
def project_update(request: AuthenticatedHttpRequest, id: int) -> HttpResponse:
    project = get_object_or_404(Project, id=id, organization=request.user.organization)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return render(request, 'projects/partials/form_success.html')
        return render(request, 'projects/partials/form.html', {'form': form})

    form = ProjectForm(instance=project)
    return render(request, 'projects/update.html', {'form': form})
