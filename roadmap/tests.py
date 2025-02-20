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


@pytest.mark.django_db
def test_roadmaps_view(client, organization, django_user_model):
    url = reverse('roadmap:roadmaps', kwargs={'slug': organization.slug})

    # Test access without login
    response = client.get(url)
    login_url = reverse('users:login')
    assertRedirects(response, f'{login_url}?next={url}')

    # Create and login user
    user = django_user_model.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')

    # Test invalid organization slug
    invalid_url = reverse('roadmap:roadmaps', kwargs={'slug': 'invalid-slug'})
    response = client.get(invalid_url)
    assert response.status_code == 404

    # Test successful POST request
    response = client.post(url, {'name': 'Test Roadmap'})
    assertRedirects(
        response, reverse('roadmap:roadmaps', kwargs={'slug': organization.slug})
    )
    assert OrganizationRoadmap.objects.filter(
        organization=organization, name='Test Roadmap'
    ).exists()

    # Test invalid POST request
    response = client.post(url, {'name': ''})
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['form'].errors
