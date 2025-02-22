# events/api.py
import calendar
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .services import GoogleCalendarService
from core.exceptions import ExpiredRefreshTokenError, GoogleNetworkError
from .models import UserCalendar
from .serializers import UserCalendarSerializer

class UserCalendarsEventsApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        calendar_service = GoogleCalendarService()
        try:
            events = calendar_service.get_all_events(request.user)
            return Response(events, status=status.HTTP_200_OK)
        except ExpiredRefreshTokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except GoogleNetworkError as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class UserCalendarsListApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user_calendars = UserCalendar.objects.filter(user=request.user)
            if not user_calendars.exists():
                return Response({"error": "У пользователя нет календарей"}, status=status.HTTP_404_NOT_FOUND)

            serializer = UserCalendarSerializer(user_calendars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserCalendar.DoesNotExist:
            return Response({"error": "Календари не найдены"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Внутренняя ошибка сервера"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateUserCalendarApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            UserCalendar.objects.filter(user=request.user).delete()
            calendar_service = GoogleCalendarService()
            calendar_service.create_user_calendars(request.user)
            user_calendars = UserCalendar.objects.filter(user=request.user)
            serializer = UserCalendarSerializer(user_calendars, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Внутренняя ошибка сервера"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ToggleUserCalendarSelectApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            calendar_id = request.data.get('calendar_id')
            calendar_service = GoogleCalendarService()
            calendar_service.toggle_calendar_select(request.user, calendar_id)
            return Response({"success": "Календарь успешно переключен"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Внутренняя ошибка сервера"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)