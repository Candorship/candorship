import os

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from integrations.google.client import GoogleAPIClient

from .forms import LoginForm, SignupForm
from .http import AuthenticatedHttpRequest
from .models import ExternalProfile, User

google_client = GoogleAPIClient(
    client_id=os.environ.get('GOOGLE_CLIENT_ID', ''),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET', ''),
    project_id=os.environ.get('GOOGLE_PROJECT_ID', ''),
    redirect_uri=os.environ.get('GOOGLE_REDIRECT_URI', ''),
    scopes=os.environ.get('GOOGLE_OAUTH_SCOPES', '').split(','),
)


def signup(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('/')

    template = 'users/signup.html'
    data = {}

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create a new user
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            # Log the user in
            login(request, user)
            return redirect('/')
        else:
            data['form'] = form
    else:
        # Pre-fill email if provided via query parameter (from Google login)
        initial = {}
        email = request.GET.get('email')
        data['reason'] = request.GET.get('reason', False)

        if email:
            initial['email'] = email

        form = SignupForm(initial=initial)
        data['form'] = form

    return render(
        request,
        template,
        data,
    )


def login_user(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.cleaned_data['user'])
            return redirect('/')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def google_login_redirect(request: HttpRequest) -> HttpResponse:
    """
    Starts the Google Login oauth flow.
    Google's response will be handled in the google_login_callback view.
    """
    url = google_client.get_oauth_authorization_url()
    return redirect(url)


def google_login_callback(request: AuthenticatedHttpRequest) -> HttpResponse:
    """
    Supports both login and signup flows.
    If the user is already signed in, we will update the user's Google OAuth credentials.
    If they are not signed in, we will create the user account and sign them in.
    """
    code = request.GET.get('code')
    creds = google_client.get_oauth_credentials(code)

    if creds is None:
        return redirect('/login')

    oauth_profile = google_client.get_user_profile(
        token=creds.token, refresh_token=creds.refresh_token
    )

    if oauth_profile.verified_email:
        # If Google is authoritative
        email = oauth_profile.email

        if request.user.is_authenticated:
            user = request.user
        else:
            # Check if there is an existing account for the user first. If not, we create it
            try:
                user = User.objects.select_related('external_profile').get(email=email)
            except User.DoesNotExist:
                user = User(
                    username=email,
                    email=email,
                    first_name=oauth_profile.given_name,
                    last_name=oauth_profile.family_name,
                )
                user.set_unusable_password()
                user.save()

        profile, created = ExternalProfile.objects.get_or_create(user=user)
        profile.google_access_token = creds.token
        profile.google_refresh_token = creds.refresh_token
        profile.google_scopes = ','.join(creds.scopes)
        profile.google_enabled = True
        profile.save()
        login(request, user)
        return redirect('/')
    else:
        # Google is not authoritative, we will need to
        # (i) Get them to create an account
        # (ii) Verify user's email manually
        return redirect(
            reverse('users:signup')
            + '?reason=unauthoritative&email='
            + oauth_profile.email
        )


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('/')


@login_required
def create_organization(request: HttpRequest) -> HttpResponse:
    return render(request, 'users/create_organization.html')
