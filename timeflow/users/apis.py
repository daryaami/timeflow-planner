from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import AuthenticationFailed


from users.services import AuthService
from .serializers import UserSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_jwt = request.COOKIES.get('refresh_jwt')
        
        if not refresh_jwt:
            return Response(
                {"error": "Refresh token not provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_jwt)
            token.blacklist()
            response =  Response(status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie('refresh_jwt')
            return response
        except Exception as e:
            return Response(
                {"error": f"Log out failed: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

class RefreshJWTView(APIView):
    """
    Обновляет access JWT токен, используя refresh токен.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_jwt = request.COOKIES.get('refresh_jwt')
        print(request.COOKIES)
        if not refresh_jwt:
            return Response(
                {"error": "No refresh token provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_jwt)
            new_access_token = str(refresh.access_token)
            return Response(
                {"access_jwt": new_access_token},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": "Invalid or expired refresh token. Please login again."},
                status=status.HTTP_401_UNAUTHORIZED
            )

class ProfileView(APIView):
    '''Получает информацию о профиле юзера'''
    permission_classes = [IsAuthenticated]

    def get(self, request):
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
            return Response({"detail": "Refresh token is absent in request cookies."},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            AuthService.verify_refresh_token(refresh_jwt)
        except AuthenticationFailed:
            return Response({"detail": "Refresh token is invalid or expired."},
                            status=status.HTTP_403_FORBIDDEN)

        # Проверка access токена
        user = request.user
        if not user or not user.is_authenticated:
            return Response({"detail": "Access token is invalid or expired."},
                            status=status.HTTP_401_UNAUTHORIZED)

        return Response({"detail": "Tokens are valid."}, status=status.HTTP_200_OK)