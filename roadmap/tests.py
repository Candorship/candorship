import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertTemplateUsed

from users.models import Organization

from .models import OrganizationRoadmap, RoadmapItem, RoadmapTimeFrame


@pytest.fixture
def organization(db):
    return Organization.objects.create(
        name='Test Org',
        slug='test-org',
        homepage_url='https://example.com',
        github_url='https://github.com/example',
    )


@pytest.fixture
def roadmap(organization):
    return OrganizationRoadmap.objects.create(
        organization=organization, name='Test Roadmap'
    )


@pytest.fixture
def time_frame(roadmap):
    return RoadmapTimeFrame.objects.create(roadmap=roadmap, name='Q1 2024')


@pytest.fixture
def roadmap_item(roadmap, time_frame):
    return RoadmapItem.objects.create(
        roadmap=roadmap,
        time_frame=time_frame,
        name='Test Feature',
        description='Test Description',
        status='PLANNED',
    )


@pytest.mark.django_db
def test_roadmap_list_view(client):
    url = reverse('roadmap:roadmap')
    response = client.get(url)
    assertTemplateUsed(response, 'roadmap/roadmap.html')


@pytest.mark.django_db
def test_roadmap_detail_view(client, organization, roadmap, time_frame, roadmap_item):
    # Invalid slug
    url = reverse('roadmap:roadmap_detail', kwargs={'slug': 'nonexistent-org'})
    response = client.get(url)
    assertRedirects(response, '/')

    # Valid slug
    url = reverse('roadmap:roadmap_detail', kwargs={'slug': organization.slug})
    response = client.get(url)

    assertTemplateUsed(response, 'roadmap/roadmap_detail.html')
    assert response.context['roadmap'] == roadmap
    assert list(response.context['time_frames']) == [time_frame]
