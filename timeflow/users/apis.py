from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from core.exceptions import ReauthRequiredError


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response("Log out failed.", status=status.HTTP_400_BAD_REQUEST)


class RefreshJWTView(APIView):
    """
    Обновляет access jwt токен, используя refresh токен.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_jwt = request.data.get("refresh_token")
        if not refresh_jwt:
            raise Exception(
                "No refresh token provided",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_jwt)
            new_access_token = str(refresh.access_token)
            return Response({"access_jwt": new_access_token})
        except Exception:
            raise ReauthRequiredError(
                "Invalid or expired refresh token. Please login again."
            )
