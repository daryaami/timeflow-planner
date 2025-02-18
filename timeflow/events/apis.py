# events/api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .services import GoogleCalendarService
from core.exceptions import ExpiredRefreshTokenError, GoogleNetworkError

class UserCalendarsEventsApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        calendar_service = GoogleCalendarService()
        try:
            events = calendar_service.get_all_events(request.user)
            return Response(events, status=status.HTTP_200_OK)
        except ExpiredRefreshTokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except GoogleNetworkError as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class GoogleCalendarsListApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        calendar_service = GoogleCalendarService()
        try:
            calendars = calendar_service.get_google_calendars(request.user)
            return Response(calendars, status=status.HTTP_200_OK)
        except ExpiredRefreshTokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except GoogleNetworkError as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

