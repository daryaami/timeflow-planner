from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


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
