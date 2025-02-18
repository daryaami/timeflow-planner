from attrs import define
import jwt
from google_auth.models import GoogleRefreshToken
from google_auth.services import GoogleAccessTokens, UserInfo, save_google_refresh_token
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from core.exceptions import ExpiredRefreshTokenError

User = get_user_model()

class AuthService:
    def __init__(self, user_info: UserInfo, google_tokens: GoogleAccessTokens):
        self.user_info = user_info
        self.google_tokens = google_tokens

    def authenticate_user(self):
        user, created = self.get_or_create_user()
        return self._generate_jwt(user), user, created
    
    def get_or_create_user(self):
        user, created = User.objects.get_or_create(
            google_id=self.user_info.sub,
            defaults={"email": self.user_info.email, "name": self.user_info.name, "picture": self.user_info.picture}
        )
        return user, created

    def _generate_jwt(self, user):
        refresh = RefreshToken.for_user(user)
        print("Generated JWT:", {"access_token": str(refresh.access_token), "refresh_token": str(refresh)})
        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }