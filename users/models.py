from django.contrib.auth.models import AbstractUser, UserManager
from django.db import IntegrityError, models
from django.db.models.signals import post_save
from django.dispatch import receiver

from db.models import BaseModel, CreatedUpdatedMixin


class Organization(BaseModel, CreatedUpdatedMixin):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='organizations/', blank=True, null=True)

    github_url = models.URLField(blank=True, null=True)
    homepage_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class User(AbstractUser, CreatedUpdatedMixin):
    id = models.AutoField(primary_key=True)
    objects: UserManager = UserManager()

    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
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


class ExternalProfile(CreatedUpdatedMixin, BaseModel):
    google_access_token = models.CharField(max_length=100, blank=True, null=True)
    google_refresh_token = models.CharField(max_length=100, blank=True, null=True)
    google_token_uri = models.CharField(max_length=255, blank=True, null=True)
    google_scopes = models.CharField(max_length=255, blank=True, null=True)
    google_enabled = models.BooleanField(default=False)

    user = models.OneToOneField(
        'users.User', on_delete=models.CASCADE, related_name='external_profile'
    )


class OrganizationUser(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    joined_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('organization', 'user')


@receiver(post_save, sender=User)
def create_external_profile(sender, instance, created, **kwargs):
    if created:
        try:
            ExternalProfile.objects.create(user=instance)
        except IntegrityError:
            pass
