# events/api.py
import requests
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from google_auth.services import get_user_token, refresh_google_access_token

class CalendarEventsApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        if not user.google_id:
            return Response({"error": "Google ID not found."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            access_token = get_user_token(user.google_id)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        google_calendar_url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
        response = requests.get(google_calendar_url, headers=headers)

        if response.status_code == 401:
            try:
                new_access_token = refresh_google_access_token(user)
                headers["Authorization"] = f"Bearer {new_access_token}"
                response = requests.get(google_calendar_url, headers=headers)
            except Exception as e:
                return Response({"error": f"Token refresh failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        if response.ok:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Failed to retrieve events from Google Calendar", "details": response.text},
                status=status.HTTP_400_BAD_REQUEST
            )
