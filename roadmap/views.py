from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def roadmap(request: HttpRequest) -> HttpResponse:
    return render(request, 'roadmap/roadmap.html')
