import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import AuthenticationFailed

from core.exceptions import RefreshJWTError
from timeflow.users.services import AuthService
from .serializers import UserSerializer

logger = logging.getLogger(__name__)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Выход пользователя и отзыв refresh токена",
        responses={
            205: openapi.Response(description="Токен успешно отозван"),
            500: "Ошибка на сервере"
        }
    )
    def post(self, request):
        refresh_jwt = request.COOKIES.get('refresh_jwt')
        if not refresh_jwt:
            logger.warning("Logout attempt without refresh token for user %s", request.user)
            raise RefreshJWTError("Logout attempt without refresh token.")
        try:
            token = RefreshToken(refresh_jwt)
            token.blacklist()
            response = Response(status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie('refresh_jwt')
            logger.info("User %s successfully logged out. Refresh token blacklisted.", request.user)
            return response
        except Exception as e:
            logger.exception("Logout failed for user %s: %s", request.user, str(e))
            return Response(
                {"error": f"Log out failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RefreshJWTView(APIView):
    """
    Обновляет access JWT токен, используя refresh токен.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Обновление access JWT токена",
        responses={
            200: openapi.Response(
                description="Access JWT токен успешно обновлен",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "access_jwt": openapi.Schema(type=openapi.TYPE_STRING, description="Access JWT токен")
                    }
                )
            ),
            403: openapi.Response(description="Refresh JWT токен не найден или истек"),
            500: "Ошибка на сервере"
        }    
    )
    def post(self, request):
        refresh_jwt = request.COOKIES.get('refresh_jwt')
        logger.debug("Received cookies for refresh: %s", request.COOKIES)
        if not refresh_jwt:
            logger.warning("Refresh token not provided in request cookies.")
            raise RefreshJWTError("Refresh token not provided in request cookies.")

        try:
            refresh = RefreshToken(refresh_jwt)
            new_access_token = str(refresh.access_token)
            logger.info("New access token generated using provided refresh token.")
            return Response(
                {"access_jwt": new_access_token},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.exception("Failed to refresh JWT: %s", str(e))
            raise RefreshJWTError(detail=str(e))

class ProfileView(APIView):
    '''Получает информацию о профиле юзера'''
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получение информации о текущем пользователе",
        responses={200: UserSerializer()}
    )
    def get(self, request):
        logger.info("User %s requested their profile.", request.user)
        user = UserSerializer(request.user)
        return Response(user.data, status=status.HTTP_200_OK)
    
class TokenPingView(APIView):
    '''Проверяет работоспособность access_jwt и refresh_jwt токенов'''
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Проверка работоспособности токена",
        responses={200: openapi.Response(description="Токен работоспособен"),
                   401: openapi.Response(description="Access JWT токен не найден или истек"),
                   403: openapi.Response(description="Refresh JWT токен не найден или истек")}
    )
    def get(self, request):
        refresh_jwt = request.COOKIES.get('refresh_jwt')
        if not refresh_jwt:
            raise RefreshJWTError("Refresh token is absent in request cookies.")
        
        try:
            AuthService.verify_refresh_token(refresh_jwt)
        except AuthenticationFailed:
            return RefreshJWTError("Refresh token is invalid or expired.")

        return Response(status=status.HTTP_200_OK)