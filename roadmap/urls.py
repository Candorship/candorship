from django.urls import path

from . import views

app_name = 'roadmap'

urlpatterns = [
    path('roadmap', views.roadmap, name='roadmap'),
    path('<str:slug>/roadmap', views.roadmap_detail, name='roadmap_detail'),
]
