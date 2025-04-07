import calendar
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.exceptions import ValidationError
from core.exceptions import GoogleAuthError, UserNotFoundError, GoogleNetworkError, InvalidGoogleResponseError, InvalidGoogleTokenError, ExpiredRefreshTokenError, GoogleTokenExchangeError, InvalidStateError
import datetime

from rest_framework.permissions import IsAuthenticated

from .services import (
    GoogleRawLoginFlowService,
)
from events.services import GoogleCalendarService
from users.services import AuthService
from .services import save_google_refresh_token
import logging
from django.db import transaction

logger = logging.getLogger(__name__)


class PublicApi(APIView):
    authentication_classes = ()
    permission_classes = ()


class GoogleLoginRedirectApi(PublicApi):
    def get(self, request, *args, **kwargs):
        try:
            consent = request.GET.get('consent', 'false').lower() == 'true'
            # consent = True
            
            google_login_flow = GoogleRawLoginFlowService()
            authorization_url, state = google_login_flow.get_authorization_url(consent=consent)

            if not authorization_url:
                return Response(
                    {"error": "Не удалось получить URL авторизации от Google."},
                    status=status.HTTP_400_BAD_REQUEST
                )

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
            with transaction.atomic():
                auth_service = AuthService(user_info, google_tokens)
                jwt_tokens, user, created = auth_service.authenticate_user()

                access_jwt, refresh_jwt = jwt_tokens['access_token'], jwt_tokens['refresh_token']

                if google_tokens.refresh_token:
                    save_google_refresh_token(user=user, refresh_token=google_tokens.refresh_token)

                if created:
                    logger.info("Создан пользователь: %s", user)
                    calendar_service = GoogleCalendarService()
                    calendar_service.create_user_calendars(user=user)

                if created and not google_tokens.refresh_token:
                    raise ExpiredRefreshTokenError()

            result = {
                "access_jwt": access_jwt,
                "created": created,
            }

            response = Response(result, status=status.HTTP_200_OK)
            
            expires = datetime.datetime.now(datetime.timezone.utc) + settings.REFRESH_TOKEN_LIFETIME
            
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
            logger.exception("InvalidGoogleTokenError при авторизации: %s", e)
            raise InvalidGoogleTokenError()
        except ExpiredRefreshTokenError as e:
            logger.exception("ExpiredRefreshTokenError при авторизации: %s", e)
            raise ExpiredRefreshTokenError()
        except GoogleNetworkError as e:
            logger.exception("GoogleNetworkError при авторизации: %s", e)
            raise GoogleNetworkError()
        except Exception as e:
            logger.exception("Неожиданная ошибка при авторизации через Google: %s", e)
            raise GoogleAuthError(detail=str(e))