# Generated by Django 5.1.6 on 2025-02-11 05:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('roadmap', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationroadmap',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roadmaps', to='users.organization'),
        ),
        migrations.AddField(
            model_name='roadmapitem',
            name='roadmap',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='roadmap.organizationroadmap'),
        ),
        migrations.AddField(
            model_name='roadmaptimeframe',
            name='roadmap',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_frames', to='roadmap.organizationroadmap'),
        ),
        migrations.AddField(
            model_name='roadmapitem',
            name='time_frame',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='roadmap.roadmaptimeframe'),
        ),
    ]
