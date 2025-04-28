from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('projects/new/', views.project_create, name='create'),
    path('projects/<int:id>/update/', views.project_update, name='update'),
]
