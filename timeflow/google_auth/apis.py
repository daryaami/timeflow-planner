from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from google_auth.serializers import GoogleAccessTokensSerializer
from rest_framework.permissions import IsAuthenticated

from .services import (
    GoogleRawLoginFlowService,
)
from users.services import AuthService
from .services import get_user_token, save_refresh_token
from users.selectors import get_user_by_google_id
from django.contrib.auth import login


class PublicApi(APIView):
    authentication_classes = ()
    permission_classes = ()

class AccessTokenApi(APIView):
    permission_classes = [IsAuthenticated]  # Доступ только для аутентифицированных пользователей

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.google_id:
            return Response({"error": "Google ID not found"}, status=status.HTTP_400_BAD_REQUEST)
        access_token = get_user_token(user.google_id)
        return Response({"access_token": access_token}, status=status.HTTP_200_OK)


class GoogleLoginRedirectApi(PublicApi):
    def get(self, request, *args, **kwargs):
        google_login_flow = GoogleRawLoginFlowService()
        authorization_url, state = google_login_flow.get_authorization_url()
        # request.session["state"] = state
        print("authorization_url", authorization_url)
        return Response({"auth_url": f"{authorization_url}"}, status=status.HTTP_200_OK)


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

        # if code is None or state is None:
        #     return Response({"error": "Code and state are required."}, status=status.HTTP_400_BAD_REQUEST)

        # session_state = request.session.get("state")

        # if session_state is None:
        #     return Response({"error": "CSRF check failed. State is not found."}, status=status.HTTP_400_BAD_REQUEST)

        # del request.session["state"]

        # if state != session_state:
        #     return Response({"error": "CSRF check failed."}, status=status.HTTP_400_BAD_REQUEST)

        google_login_flow = GoogleRawLoginFlowService()
        google_tokens = google_login_flow.get_tokens(code=code)
        google_tokens_data = GoogleAccessTokensSerializer(google_tokens).data

        user_info = google_login_flow.get_user_info(google_tokens=google_tokens)

        google_auth_service = AuthService(user_info, google_tokens)
        jwt_tokens, user, created = google_auth_service.authenticate_user()
        access_jwt, refresh_jwt = jwt_tokens['access_token'], jwt_tokens['refresh_token']

        if created:
            save_refresh_token(user=user, refresh_token=google_tokens.refresh_token)

        result = {
            "access_jwt": access_jwt,
            "refresh_jwt": refresh_jwt,
            "created": created,
        }

        return Response(result, status=status.HTTP_200_OK)