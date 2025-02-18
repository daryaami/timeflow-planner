from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from core.exceptions import GoogleAuthError, UserNotFoundError, GoogleNetworkError, InvalidGoogleResponseError, InvalidGoogleTokenError, ExpiredRefreshTokenError, GoogleTokenExchangeError, InvalidStateError

from rest_framework.permissions import IsAuthenticated

from .services import (
    GoogleRawLoginFlowService,
)
from users.services import AuthService
from .services import get_user_token, save_google_refresh_token, refresh_google_access_token


class AccessTokenApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.google_id:
            raise UserNotFoundError("Google ID not found")

        try:
            access_token = get_user_token(user.google_id)
            return Response({"access_token": access_token}, status=status.HTTP_200_OK)
        except Exception:
            # Попытка обновления access_token через refresh_token
            refresh_result = refresh_google_access_token(user)
            if "reauth_required" in refresh_result:
                # Выбрасываем исключение, которое даст понять фронтенду,
                # что нужно заново залогиниться
                raise ExpiredRefreshTokenError(
                    "Access token expired and refresh token invalid. Please login again.",)
            return Response({"access_token": refresh_result["access_token"]}, status=status.HTTP_200_OK)


class PublicApi(APIView):
    authentication_classes = ()
    permission_classes = ()


class GoogleLoginRedirectApi(PublicApi):
    def get(self, request, *args, **kwargs):
        try:
            google_login_flow = GoogleRawLoginFlowService()
            authorization_url, state = google_login_flow.get_authorization_url()

            if not authorization_url:
                raise GoogleAuthError("Не удалось получить URL авторизации от Google.")

            return Response({"auth_url": authorization_url}, status=status.HTTP_200_OK)
        
        except Exception as e:
            raise GoogleAuthError(f"Ошибка при запросе авторизации: {str(e)}")


class GoogleLoginApi(PublicApi):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)
        state = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get("code")
        error = validated_data.get("error")
        state = validated_data.get("state")

        if error is not None:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        if code is None or state is None:
            return Exception("Code and state are required.", status=status.HTTP_400_BAD_REQUEST)

        # session_state = request.session.get("state")

        # if session_state is None:
        #     return Response({"error": "CSRF check failed. State is not found."}, status=status.HTTP_400_BAD_REQUEST)

        # del request.session["state"]

        # if state != session_state:
        #     return Response({"error": "CSRF check failed."}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем GoogleRawLoginFlowService для получения токенов и информации о пользователе
        google_login_flow = GoogleRawLoginFlowService()
        google_tokens = google_login_flow.get_tokens(code=code)

        user_info = google_login_flow.get_user_info(google_tokens=google_tokens)

        # Аутентифицируем пользователя
        auth_service = AuthService(user_info, google_tokens)
        jwt_tokens, user, created = auth_service.authenticate_user()
        access_jwt, refresh_jwt = jwt_tokens['access_token'], jwt_tokens['refresh_token']

        if created:
            save_google_refresh_token(user=user, refresh_token=google_tokens.refresh_token)

        result = {
            "access_jwt": access_jwt,
            "refresh_jwt": refresh_jwt,
            "created": created,
        }

        return Response(result, status=status.HTTP_200_OK)