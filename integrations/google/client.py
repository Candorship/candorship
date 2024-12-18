import logging
from typing import Dict, List

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

logger = logging.getLogger('candorship')


class OAuthCredentials:
    token: str
    refresh_token: str
    scopes: List[str]

    def __init__(self, token: str, refresh_token: str, scopes: List[str]):
        self.token = token
        self.refresh_token = refresh_token
        self.scopes = scopes


class OAuthUserInfo:
    email: str
    family_name: str
    given_name: str

    def __init__(
        self,
        email: str,
        given_name: str,
        family_name: str,
    ):
        self.email = email
        self.family_name = family_name
        self.given_name = given_name


class GoogleAPIClient(object):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        project_id: str,
        scopes: List[str],
        redirect_uri: str,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.project_id = project_id
        self.scopes = scopes
        self.redirect_uri = redirect_uri

        credentials = {
            'web': {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'project_id': self.project_id,
                'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                'token_uri': 'https://oauth2.googleapis.com/token',
            }
        }

        self.flow = Flow.from_client_config(
            credentials,
            scopes=self.scopes,
            redirect_uri=self.redirect_uri,
        )

    def get_oauth_authorization_url(self) -> str:
        url, state = self.flow.authorization_url(
            access_type='offline', include_granted_scopes='false', prompt='consent'
        )
        return url

    def get_oauth_credentials(self, code) -> OAuthCredentials | None:
        self.flow.fetch_token(code=code)
        creds = self.flow.credentials

        if not creds.refresh_token or not creds.token:
            logger.error('No refresh token found')
            return None

        return OAuthCredentials(
            token=creds.token,
            refresh_token=creds.refresh_token,
            scopes=self.scopes,
        )

    def get_user_profile(self, token, refresh_token) -> OAuthUserInfo:
        creds = Credentials.from_authorized_user_info(
            {
                'token': token,
                'scopes': self.scopes,
                'refresh_token': refresh_token,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
            }
        )

        user_info_service = build('oauth2', 'v2', credentials=creds)
        user_info = user_info_service.userinfo().get().execute()

        return OAuthUserInfo(
            email=user_info.get('email'),
            family_name=user_info.get('family_name'),
            given_name=user_info.get('given_name'),
        )
