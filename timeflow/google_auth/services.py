from random import SystemRandom

from typing import Any, Dict
from urllib.parse import urlencode
import jwt
import requests
from attrs import define
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.cache import cache
from oauthlib.common import UNICODE_ASCII_CHARACTER_SET
from core.exceptions import ExpiredRefreshTokenError, InvalidGoogleTokenError, GoogleNetworkError, RefreshTokenError
from rest_framework import status

from django.core.cache import cache

from google_auth.models import GoogleRefreshToken

@define(kw_only=True, slots=True)
class UserInfo:
    sub: str
    email: str
    email_verified: bool
    name: str
    given_name: str | None = None
    family_name: str | None = None
    picture: str | None = None

@define
class GoogleRawLoginCredentials:
    client_id: str
    client_secret: str
    project_id: str


@define(kw_only=True, slots=True)
class GoogleAccessTokens:
    id_token: str | None = None
    access_token: str
    refresh_token: str | None = None
    expires_in: int | None = 3600

    def decode_id_token(self) -> Dict[str, str]:
        return jwt.decode(jwt=self.id_token, options={"verify_signature": False})


class GoogleRawLoginFlowService:
    API_URI = settings.GOOGLE_API_URI
    
    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
    GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    SCOPES = [
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/calendar.events",
    ]

    def __init__(self):
        self._credentials = google_raw_login_get_credentials()

    @staticmethod
    def _generate_state_session_token(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
        # This is how it's implemented in the official SDK
        rand = SystemRandom()
        state = "".join(rand.choice(chars) for _ in range(length))
        return state

    def _get_redirect_uri(self):
        return self.API_URI

    def get_authorization_url(self, consent=False):
        redirect_uri = self._get_redirect_uri()

        state = self._generate_state_session_token()

        params = {
            "response_type": "code",
            "client_id": self._credentials.client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(self.SCOPES),
            "state": state,
            "access_type": "offline",
            "include_granted_scopes": "true",
        }

        if consent:
            params["prompt"] = "consent"

        query_params = urlencode(params)
        authorization_url = f"{self.GOOGLE_AUTH_URL}?{query_params}"

        return authorization_url, state

    def get_tokens(self, *, code: str) -> GoogleAccessTokens:
        '''
        Метод для получения access_token и refresh_token и сохранения access_token в кэше
        '''
        redirect_uri = self._get_redirect_uri()

        # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#obtainingaccesstokens
        data = {
            "code": code,
            "client_id": self._credentials.client_id,
            "client_secret": self._credentials.client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
            "access_type": "offline",
            "include_granted_scopes": "true",
        }

        response = requests.post(self.GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

        if not response.ok:
            raise InvalidGoogleTokenError("Failed to obtain access token from Google.")

        tokens = response.json()
        google_tokens = GoogleAccessTokens(id_token=tokens.get("id_token"), 
                                           access_token=tokens.get("access_token"), 
                                           refresh_token=tokens.get("refresh_token", None), 
                                           expires_in=tokens.get("expires_in", None))
        store_user_token(user_id=google_tokens.decode_id_token()["sub"], token=google_tokens.access_token, expires_in=google_tokens.expires_in)

        return google_tokens

    def get_user_info(self, *, google_tokens: GoogleAccessTokens) -> Dict[str, Any]:
        access_token = google_tokens.access_token
        # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#callinganapi
        response = requests.get(self.GOOGLE_USER_INFO_URL, params={"access_token": access_token})

        if not response.ok:
            raise GoogleNetworkError("Failed to obtain user info from Google.")
        
        print(response.json())
        user_info = UserInfo(**response.json())

        return user_info
        
    def refresh_access_token(self, *, refresh_token: str) -> GoogleAccessTokens:
        """
        Обновляет access_token с использованием refresh_token.
        """
        data = {
            "client_id": self._credentials.client_id,
            "client_secret": self._credentials.client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }
        response = requests.post(self.GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)
        if not response.ok:
            raise RefreshTokenError("Failed to refresh access token from Google.")
        tokens = response.json()
        # Обратите внимание, что в ответе может не быть id_token
        new_tokens = GoogleAccessTokens(id_token=tokens.get("id_token"), 
                                        access_token=tokens.get("access_token"), 
                                        refresh_token=tokens.get("refresh_token", None), 
                                        expires_in=tokens.get("expires_in", None))

        # Обновляем access_token в кэше
        # Здесь decoded_token["sub"] можно получить через сохранённого пользователя
        # Поэтому оставим caller'у ответственность за передачу user_id
        # store_user_token(user_id=user_id, token=new_tokens.access_token, expires_in=new_tokens.expires_in)

        return new_tokens


# Можно перенести в класс?
def google_raw_login_get_credentials() -> GoogleRawLoginCredentials:    
    client_id = settings.GOOGLE_OAUTH2_CLIENT_ID
    client_secret = settings.GOOGLE_OAUTH2_CLIENT_SECRET
    project_id = settings.GOOGLE_OAUTH2_PROJECT_ID

    if not client_id:
        raise ImproperlyConfigured("GOOGLE_OAUTH2_CLIENT_ID missing in env.")

    if not client_secret:
        raise ImproperlyConfigured("GOOGLE_OAUTH2_CLIENT_SECRET missing in env.")

    if not project_id:
        raise ImproperlyConfigured("GOOGLE_OAUTH2_PROJECT_ID missing in env.")

    credentials = GoogleRawLoginCredentials(client_id=client_id, client_secret=client_secret, project_id=project_id)

    return credentials


def store_user_token(user_id: str, token: str, expires_in: int = 3600):
    """
    Сохраняет access_token для пользователя с указанным user_id.
    expires_in - время жизни токена в секундах (по умолчанию 1 час).
    """
    key = f"google_access_token_{user_id}"
    cache.set(key, token, timeout=expires_in - 60)  # Сохранение с запасом 1 минута


def get_user_token(user_id: str):
    """
    Получает access_token пользователя по user_id.
    """
    key = f"google_access_token_{user_id}"
    token = cache.get(key)
    if not token:
        raise InvalidGoogleTokenError("Access token expired or not found.")
    return token


def save_google_refresh_token(user, refresh_token):
    GoogleRefreshToken.objects.update_or_create(
        user=user, 
        defaults={"refresh_token": refresh_token}
    )


def refresh_google_access_token(user):
    """
    Обновляет access_token для пользователя, используя сохранённый refresh_token.
    Если refresh_token не работает, выбрасывается исключение,
    которое сообщит фронтенду, что требуется повторная авторизация.
    """
    try:
        g_refresh_token = GoogleRefreshToken.objects.get(user=user)
    except GoogleRefreshToken.DoesNotExist:
        raise ExpiredRefreshTokenError(
            "Refresh token not found for user. Please login again.",)

    google_login_flow = GoogleRawLoginFlowService()

    try:
        new_tokens = google_login_flow.refresh_access_token(refresh_token=g_refresh_token.refresh_token)
    except Exception:
        raise RefreshTokenError(
            "Failed to refresh access token. Please login again."
        )

    store_user_token(user_id=user.google_id, token=new_tokens.access_token, expires_in=new_tokens.expires_in)
    
    return {"access_token": new_tokens.access_token}
