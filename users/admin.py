from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DJUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import ExternalProfile, Organization, OrganizationUser, User


class UserAdmin(DJUserAdmin):
    list_display = (
        'email',
        'first_name',
        'is_staff',
        'is_superuser',
    )


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')


class ExternalProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'google_enabled', 'created_at', 'updated_at')
    list_filter = ('google_enabled',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')


class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'joined_date')
    list_filter = ('organization',)
    search_fields = ('user__email', 'organization__name')
    raw_id_fields = ('user', 'organization')


admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(ExternalProfile, ExternalProfileAdmin)
admin.site.register(OrganizationUser, OrganizationUserAdmin)
