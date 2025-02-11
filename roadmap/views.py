from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

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
