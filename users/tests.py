import json
from unittest.mock import patch

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertTemplateUsed

from .models import ExternalProfile, User


@pytest.mark.django_db
def test_users():
    u = User.objects.create(username='testuser', email='test@email.com')

    with pytest.raises(Exception):
        u.set_manager(u)


@pytest.mark.django_db
def test_signup(client, user1):
    url = reverse('users:signup')
    resp = client.get(url)
    assertTemplateUsed(resp, 'users/signup.html')

    client.force_login(user1)

    resp = client.get(url)
    assertRedirects(resp, '/')


@pytest.mark.django_db
def test_login(client, user1):
    url = reverse('users:login')
    resp = client.get(url)
    assertTemplateUsed(resp, 'users/login.html')

    client.force_login(user1)

    resp = client.get(url)
    assertTemplateUsed(resp, 'users/login.html')


@pytest.mark.django_db
def test_logout(client, user1):
    logout_url = reverse('users:logout')

    client.force_login(user1)
    resp = client.get(logout_url)
    assertRedirects(resp, '/')


@pytest.mark.django_db
@patch('users.views.GoogleAPIClient.get_oauth_authorization_url')
def test_google_login_redirect(mock_get_oauth_authorization_url, client):
    mock_get_oauth_authorization_url.return_value = '/oauth'
    url = reverse('users:google-login-redirect')
    response = client.get(url)
    assertRedirects(response, '/oauth', fetch_redirect_response=False)


@pytest.mark.django_db
@patch('users.views.GoogleAPIClient.get_oauth_credentials')
@patch('users.views.GoogleAPIClient.get_user_profile')
def test_google_login_callback(
    mock_get_user_profile, mock_get_oauth_credentials, client
):
    mock_get_oauth_credentials.return_value = {
        'token': 'fake-token',
        'refresh_token': 'fake-refresh-token',
        'scopes': json.dumps(['scope1', 'scope2']),
    }
    mock_get_user_profile.return_value = {
        'email': 'testuser@example.com',
        'given_name': 'Test',
        'family_name': 'User',
    }

    url = reverse('users:google-login-callback')
    response = client.get(url, {'code': 'fake-code'})

    assertRedirects(response, '/')
    user = User.objects.get(email='testuser@example.com')
    assert user.first_name == 'Test'
    assert user.last_name == 'User'
    profile = ExternalProfile.objects.get(user=user)
    assert profile.google_access_token == 'fake-token'
    assert profile.google_refresh_token == 'fake-refresh-token'
    assert profile.google_scopes
    google_scopes = json.loads(profile.google_scopes)
    assert 'scope1' in google_scopes
    assert 'scope2' in google_scopes
    assert profile.google_enabled
