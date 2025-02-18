from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.exceptions import ValidationError
from core.exceptions import GoogleAuthError, UserNotFoundError, GoogleNetworkError, InvalidGoogleResponseError, InvalidGoogleTokenError, ExpiredRefreshTokenError, GoogleTokenExchangeError, InvalidStateError
from datetime import datetime, timedelta

from rest_framework.permissions import IsAuthenticated

from .services import (
    GoogleRawLoginFlowService,
)
from users.services import AuthService
from .services import get_user_token, save_google_refresh_token, refresh_google_access_token


# Удалить этот эндпоинт, он тестовый
class AccessTokenApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.google_id:
            return Response(
                {"error": "Google ID not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            access_token = get_user_token(user.google_id)
            return Response({"access_token": access_token}, status=status.HTTP_200_OK)
        except Exception:
            # Попытка обновления access_token через refresh_token
            try:    
                refresh_result = refresh_google_access_token(user)
                return Response({"access_token": refresh_result["access_token"]}, status=status.HTTP_200_OK)
            except ExpiredRefreshTokenError:
                return Response(
                    {"error": "Access token expired and refresh token invalid. Please login again."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

class PublicApi(APIView):
    authentication_classes = ()
    permission_classes = ()


class GoogleLoginRedirectApi(PublicApi):
    # Для вызова с prompt=consent вызываем с параметром /?consent=true
    def get(self, request, *args, **kwargs):
        try:
            consent = request.GET.get('consent', 'false').lower() == 'true'
            
            google_login_flow = GoogleRawLoginFlowService()
            authorization_url, state = google_login_flow.get_authorization_url(consent=consent)

            if not authorization_url:
                return Response(
                    {"error": "Не удалось получить URL авторизации от Google."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response({"auth_url": authorization_url}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {"error": f"Ошибка при запросе авторизации: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


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
            return Response(
                {"error": "Code and state are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # session_state = request.session.get("state")

        # if session_state is None:
        #     return Response({"error": "CSRF check failed. State is not found."}, status=status.HTTP_400_BAD_REQUEST)

        # del request.session["state"]

        # if state != session_state:
        #     return Response({"error": "CSRF check failed."}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем GoogleRawLoginFlowService для получения токенов и информации о пользователе
        try:
            google_login_flow = GoogleRawLoginFlowService()
            google_tokens = google_login_flow.get_tokens(code=code)

            user_info = google_login_flow.get_user_info(google_tokens=google_tokens)

            # Аутентифицируем пользователя
            auth_service = AuthService(user_info, google_tokens)
            jwt_tokens, user, created = auth_service.authenticate_user()
            access_jwt, refresh_jwt = jwt_tokens['access_token'], jwt_tokens['refresh_token']

            if created or google_tokens.refresh_token:
                save_google_refresh_token(user=user, refresh_token=google_tokens.refresh_token)

            result = {
                "access_jwt": access_jwt,
                "refresh_jwt": refresh_jwt,
                "created": created,
            }

            response = Response(result, status=status.HTTP_200_OK)
            
            expires = datetime.utcnow() + settings.REFRESH_TOKEN_LIFETIME
            
            # Устанавливаем refresh token в HttpOnly cookie
            response.set_cookie(
                key='refresh_jwt',
                value=refresh_jwt,
                httponly=True,       # Доступ к куке только через HTTP(S)
                # secure=True,         # Отправлять только по HTTPS (в режиме разработки можно отключить)
                samesite='Strict',   # Ограничение для кросс-сайтовых запросов
                expires=expires
            )

            return response
        
        except InvalidGoogleTokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except GoogleNetworkError as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except ExpiredRefreshTokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except InvalidStateError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)