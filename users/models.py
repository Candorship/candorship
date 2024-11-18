from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from db.models import BaseModel, CreatedUpdatedMixin


class Organization(BaseModel, CreatedUpdatedMixin):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='organizations/', blank=True, null=True)

    def __str__(self):
        return self.name


class User(AbstractUser, CreatedUpdatedMixin):
    id = models.AutoField(primary_key=True)
    objects: UserManager = UserManager()

    email = models.EmailField(unique=True)
    organizations = models.ManyToManyField(
        Organization, related_name='users', through='OrganizationUser'
    )
    profile_photo = models.ImageField(
        upload_to='profile_photos/', blank=True, null=True
    )

    def __str__(self):
        return f'{self.name}: {self.email}'

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'


class OrganizationUser(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    joined_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('organization', 'user')
