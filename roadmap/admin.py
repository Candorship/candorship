from django.contrib import admin

from .models import OrganizationRoadmap, RoadmapItem, RoadmapTimeFrame


class OrganizationRoadmapAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'created_at', 'updated_at']
    search_fields = ['name', 'organization__name']
    list_filter = ['organization']


class RoadmapTimeFrameAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'roadmap',
        'start_date',
        'end_date',
        'created_at',
        'updated_at',
    ]
    search_fields = ['name', 'roadmap__name']
    list_filter = ['roadmap', 'start_date', 'end_date']


class RoadmapItemAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'roadmap',
        'time_frame',
        'status',
        'created_at',
        'updated_at',
    ]
    search_fields = ['name', 'description', 'roadmap__name']
    list_filter = ['status', 'roadmap', 'time_frame']


admin.site.register(OrganizationRoadmap, OrganizationRoadmapAdmin)
admin.site.register(RoadmapTimeFrame, RoadmapTimeFrameAdmin)
admin.site.register(RoadmapItem, RoadmapItemAdmin)
