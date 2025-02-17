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
from core.exceptions import ApplicationError

from django.core.cache import cache

from google_auth.models import GoogleRefreshToken


@define
class GoogleRawLoginCredentials:
    client_id: str
    client_secret: str
    project_id: str


@define
class GoogleAccessTokens:
    id_token: str
    access_token: str
    refresh_token: str

    def decode_id_token(self) -> Dict[str, str]:
        id_token = self.id_token
        decoded_token = jwt.decode(jwt=id_token, options={"verify_signature": False})
        return decoded_token


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
            raise ApplicationError("Failed to obtain access token from Google.")

        tokens = response.json()
        google_tokens = GoogleAccessTokens(id_token=tokens["id_token"], access_token=tokens["access_token"], refresh_token=tokens["refresh_token"] if "refresh_token" in tokens else None)

        expires_in = tokens.get("expires_in", 3600)  
        store_user_token(user_id=google_tokens.decode_id_token()["sub"], token=google_tokens.access_token, expires_in=expires_in)

        return google_tokens

    def get_user_info(self, *, google_tokens: GoogleAccessTokens) -> Dict[str, Any]:
        access_token = google_tokens.access_token
        # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#callinganapi
        response = requests.get(self.GOOGLE_USER_INFO_URL, params={"access_token": access_token})

        if not response.ok:
            raise ApplicationError("Failed to obtain user info from Google.")

        return response.json()
        
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
            raise ApplicationError("Failed to refresh access token from Google.")
        tokens = response.json()
        # Обратите внимание, что в ответе может не быть id_token
        new_tokens = GoogleAccessTokens(
            id_token=tokens.get("id_token", ""),
            access_token=tokens["access_token"],
            refresh_token=refresh_token  # refresh_token обычно не меняется
        )
        expires_in = tokens.get("expires_in", 3600)
        # Обновляем access_token в кэше
        # Здесь decoded_token["sub"] можно получить через сохранённого пользователя
        # Поэтому оставим caller'у ответственность за передачу user_id
        return new_tokens


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
        raise Exception("Access token expired or not found.")
    return token


def save_google_refresh_token(user, refresh_token):
    GoogleRefreshToken.objects.update_or_create(
        user=user, 
        defaults={"refresh_token": refresh_token}
    )

def refresh_google_access_token(user):
    """
    Обновляет access_token для пользователя, используя сохранённый refresh_token.
    Если refresh_token не работает, возвращает URL для повторной авторизации с prompt=consent.
    """
    try:
        g_refresh_token = GoogleRefreshToken.objects.get(user=user)
    except GoogleRefreshToken.DoesNotExist:
        raise ApplicationError("Refresh token not found for user.")

    google_login_flow = GoogleRawLoginFlowService()

    try:
        new_tokens = google_login_flow.refresh_access_token(refresh_token=g_refresh_token.refresh_token)
    except ApplicationError:
        # Если обновление токена не удалось, просим пользователя заново авторизоваться
        authorization_url, _ = google_login_flow.get_authorization_url(consent=True)
        return {"reauth_required": True, "auth_url": authorization_url}

    expires_in = 3600
    store_user_token(user_id=user.google_id, token=new_tokens.access_token, expires_in=expires_in)
    
    return {"access_token": new_tokens.access_token}
