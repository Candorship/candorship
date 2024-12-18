from django.urls import path

from . import views

app_name = 'roadmap'

urlpatterns = [
    path('roadmap', views.roadmap, name='roadmap'),
]
