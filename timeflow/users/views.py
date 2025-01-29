from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests

from django.http import JsonResponse

from .services import verify_jwt_token
from core.exceptions import ApplicationError

class GoogleCalendarEventsApi(APIView):
    def get(self, request, *args, **kwargs):
        # Получаем JWT токен из заголовка Authorization
        # auth_header = request.headers.get('Authorization')
        # if not auth_header or not auth_header.startswith('Bearer '):
        #     return Response({"error": "Authorization header missing or invalid."}, status=status.HTTP_401_UNAUTHORIZED)

        # jwt_token = auth_header.split(' ')[1]

        # try:
        #     user_data = verify_jwt_token(jwt_token)
        # except ApplicationError as e:
        #     return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        # Получаем access_token из кеша
        access_token = cache.get("google_access_token")
        if not access_token:
            return Response({"error": "Access token expired or not found."}, status=status.HTTP_401_UNAUTHORIZED)

        # Делаем запрос к Google Calendar API для получения событий
        google_calendar_api_url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.get(google_calendar_api_url, headers=headers)

        if response.status_code != 200:
            return Response({"error": "Failed to fetch calendar events."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        events = response.json().get("items", [])
        print(events)

        # return JsonResponse({"events": events}, status=status.HTTP_200_OK)
        return Response({"events": events}, status=status.HTTP_200_OK)
