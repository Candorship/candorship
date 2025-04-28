from django.db import models

from db.models import BaseModel, CreatedUpdatedMixin
from users.models import Organization


class Project(CreatedUpdatedMixin, BaseModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='projects'
    )
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=50,
        choices=[
            ('planning', 'Planning'),
            ('In Progress', 'In Progress'),
            ('completed', 'Completed'),
            ('archived', 'archived'),
        ],
        default='planning',
    )

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} for {self.organization}'
