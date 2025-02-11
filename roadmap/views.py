from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from users.models import Organization

from .forms import RoadmapForm
from .models import OrganizationRoadmap


def roadmap(request: HttpRequest) -> HttpResponse:
    return render(request, 'roadmap/roadmap.html')


def roadmap_detail(request: HttpRequest, slug: str) -> HttpResponse:
    qs = OrganizationRoadmap.objects.select_related('organization')

    try:
        roadmap = qs.get(organization__slug=slug)
    except OrganizationRoadmap.DoesNotExist:
        return redirect('/')

    time_frames = roadmap.time_frames.prefetch_related('items').order_by('id').all()

    return render(
        request,
        'roadmap/roadmap_detail.html',
        {'roadmap': roadmap, 'time_frames': time_frames},
    )


@login_required
def roadmaps(request: HttpRequest, slug: str) -> HttpResponse:
    organization = get_object_or_404(Organization, slug=slug)
    roadmaps = OrganizationRoadmap.objects.filter(organization=organization)

    if request.method == 'POST':
        form = RoadmapForm(request.POST)
        if form.is_valid():
            roadmap = form.save(commit=False)
            roadmap.organization = organization
            roadmap.save()
            messages.success(request, 'Roadmap created successfully.')
            return redirect('roadmap:roadmaps', slug=slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RoadmapForm()

    return render(
        request,
        'roadmap/roadmaps.html',
        {'form': form, 'organization': organization, 'roadmaps': roadmaps},
    )


@login_required
def edit_roadmap(request: HttpRequest, slug: str, roadmap_id: int) -> HttpResponse:
    organization = get_object_or_404(Organization, slug=slug)
    roadmap = get_object_or_404(
        OrganizationRoadmap, id=roadmap_id, organization=organization
    )

    if request.method == 'POST':
        form = RoadmapForm(request.POST, instance=roadmap)
        if form.is_valid():
            form.save()
            messages.success(request, 'Roadmap updated successfully.')
            return redirect('roadmap:roadmap_detail', slug=slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RoadmapForm(instance=roadmap)

    return render(
        request,
        'roadmap/edit_roadmap.html',
        {'form': form, 'organization': organization, 'roadmap': roadmap},
    )
