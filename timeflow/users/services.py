import jwt
from google_auth.models import GoogleRefreshToken
from google_auth.services import save_google_refresh_token
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from core.exceptions import ExpiredRefreshTokenError

User = get_user_model()

class AuthService:
    def __init__(self, user_info, google_tokens):
        self.user_info = user_info
        self.google_tokens = google_tokens

    def authenticate_user(self):
        user, created = self.get_or_create_user()

        if created:
            if self.google_tokens.refresh_token:
                save_google_refresh_token(user, self.google_tokens.refresh_token)
            else:
                raise ExpiredRefreshTokenError("Refresh token not found.")

        return self._generate_jwt(user), user, created
    
    def get_or_create_user(self):
        user, created = User.objects.get_or_create(
            google_id=self.user_info.get("sub"),
            defaults={"email": self.user_info.get("email"), "name": self.user_info.get("name"), "image": self.user_info.get("picture")}
        )
        return user, created

    def _generate_jwt(self, user):
        refresh = RefreshToken.for_user(user)
        print("Generated JWT:", {"access_token": str(refresh.access_token), "refresh_token": str(refresh)})
        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }

# def verify_jwt_token(token: str) -> dict:
#     try:
#         decoded_token = jwt.decode(
#             token,
#             settings.SECRET_KEY, 
#             algorithms=["HS256"],
#         )
#         print("Decoded JWT:", decoded_token)  # Логируем результат
#         return decoded_token
#     except jwt.ExpiredSignatureError:
#         raise ApplicationError("JWT Token has expired.")
#     except jwt.InvalidTokenError:
#         raise ApplicationError("Invalid JWT Token.")
