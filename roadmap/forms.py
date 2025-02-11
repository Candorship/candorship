from django import forms
from .models import OrganizationRoadmap, RoadmapTimeFrame, RoadmapItem

class RoadmapForm(forms.ModelForm):
    class Meta:
        model = OrganizationRoadmap
        fields = ['name']