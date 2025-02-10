from django.db import models

from db.models import BaseModel, CreatedUpdatedMixin
from users.models import Organization


class OrganizationRoadmap(CreatedUpdatedMixin, BaseModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='roadmaps'
    )
    name = models.CharField(max_length=255, null=False, blank=False)


class RoadmapTimeFrame(CreatedUpdatedMixin, BaseModel):
    roadmap = models.ForeignKey(
        'OrganizationRoadmap', on_delete=models.CASCADE, related_name='time_frames'
    )
    name = models.CharField(max_length=255, null=False, blank=False)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)


class RoadmapItem(CreatedUpdatedMixin, BaseModel):
    roadmap_status = (
        ('PLANNED', 'Planned'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )

    roadmap = models.ForeignKey(
        'OrganizationRoadmap', on_delete=models.CASCADE, related_name='items'
    )
    time_frame = models.ForeignKey(
        'RoadmapTimeFrame', on_delete=models.CASCADE, related_name='items'
    )
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=255, null=False, blank=False)
