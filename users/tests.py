import json
from unittest.mock import MagicMock, patch

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
    # Test case when verified_email is False
    mock_get_oauth_credentials.return_value = MagicMock(
        token='fake-token',
        refresh_token='fake-refresh-token',
        scopes=['scope1', 'scope2'],
    )
    mock_get_user_profile.return_value = MagicMock(
        email='testuser@example.com',
        given_name='Test',
        family_name='User',
        verified_email=False,
    )

    url = reverse('users:google-login-callback')
    response = client.get(url, {'code': 'fake-code'})

    # Should redirect to signup with email parameter
    expected_redirect = (
        reverse('users:signup') + '?reason=unauthoritative&email=testuser@example.com'
    )
    assertRedirects(response, expected_redirect)

    # Verify no user was created
    assert not User.objects.filter(email='testuser@example.com').exists()

    # Test case when verified_email is True but user already exists
    mock_get_oauth_credentials.return_value = MagicMock(
        token='fake-token',
        refresh_token='fake-refresh-token',
        scopes=['scope1', 'scope2'],
    )
    mock_get_user_profile.return_value = MagicMock(
        email='testuser@example.com',
        given_name='Test',
        family_name='User',
        verified_email=True,
    )

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

    google_scopes = profile.google_scopes.split(',')
    assert 'scope1' in google_scopes
    assert 'scope2' in google_scopes
    assert profile.google_enabled


@patch('integrations.google.client.Credentials')
@patch('integrations.google.client.build')
def test_get_user_profile(mock_build, mock_credentials, client):
    from integrations.google.client import GoogleAPIClient, OAuthUserInfo

    # Setup mock API client
    api_client = GoogleAPIClient(
        client_id='fake-client-id',
        client_secret='fake-client-secret',
        project_id='fake-project-id',
        scopes=['fake-scope'],
        redirect_uri='https://example.com/callback',
    )

    # Setup mock user info service
    mock_userinfo = MagicMock()
    mock_service = MagicMock()
    mock_service.userinfo.return_value = mock_userinfo
    mock_build.return_value = mock_service

    # Reusable test function
    def run_test_case(email, hd, expected_verified):
        user_info = {
            'email': email,
            'family_name': 'User',
            'given_name': 'Test',
            'hd': hd,
        }

        mock_userinfo.get.return_value.execute.return_value = user_info

        # Call the function
        result = api_client.get_user_profile('fake-token', 'fake-refresh-token')

        # Assertions
        assert isinstance(result, OAuthUserInfo)
        assert result.email == email
        assert result.family_name == 'User'
        assert result.given_name == 'Test'
        assert result.verified_email == expected_verified

    # Test case 1: Gmail account should be verified
    run_test_case('test@gmail.com', '', True)

    # Test case 2: G Suite account with matching domain in hd should be verified
    run_test_case('test@company.com', 'company.com', True)

    # Test case 3: Email with non-matching domain and hd should not be verified
    run_test_case('test@company.com', 'different.com', False)

    # Test case 4: Non-Gmail account without hd should not be verified
    run_test_case('test@example.com', '', False)

    # Verify Credentials was called with the right parameters
    mock_credentials.from_authorized_user_info.assert_called_with(
        {
            'token': 'fake-token',
            'scopes': ['fake-scope'],
            'refresh_token': 'fake-refresh-token',
            'client_id': 'fake-client-id',
            'client_secret': 'fake-client-secret',
        }
    )
