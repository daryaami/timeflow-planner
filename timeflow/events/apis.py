# events/api.py
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .services import GoogleCalendarService
from core.exceptions import ExpiredGoogleRefreshTokenError, GoogleAuthError, GoogleNetworkError
from .models import UserCalendar
from .serializers import GoogleCalendarEventSerializer, UserCalendarSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class UserCalendarEventsApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить события для активных календарей пользователя",
        manual_parameters=[
            openapi.Parameter('start', openapi.IN_QUERY, description="Дата начала (%Y-%m-%d)", type=openapi.TYPE_STRING),
            openapi.Parameter('end', openapi.IN_QUERY, description="Дата окончания (%Y-%m-%d)", type=openapi.TYPE_STRING),
        ],
        responses={
            200: GoogleCalendarEventSerializer(many=True),
            400: openapi.Response('Неверный формат дат или отсутствуют параметры start и end', examples={
                'application/json': {"error": "Параметры start и end обязательны"}
            }),
            500: openapi.Response('Ошибка сервера')
        }
    )
    def get(self, request, *args, **kwargs):
        '''Получить события для активных календарей пользователя'''
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        if not start or not end:
            return Response({"error": "Параметры start и end обязательны"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Преобразуем входящие даты в формат RFC3339 (ISO8601)
            start_dt = datetime.strptime(start, "%Y-%m-%d")
            end_dt = datetime.strptime(end, "%Y-%m-%d")
            time_min = start_dt.isoformat() + "Z"
            time_max = end_dt.isoformat() + "Z"
        except ValueError:
            return Response({"error": "Неверный формат дат. Ожидается YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)
        
        calendar_service = GoogleCalendarService()
        try:
            events = calendar_service.get_all_events(request.user, time_min, time_max)
            return Response(events, status=status.HTTP_200_OK)
        except ExpiredGoogleRefreshTokenError as e:
            raise e
        except GoogleNetworkError as e:
            raise e
        except Exception as e:
            raise GoogleAuthError(detail=str(e))
        
    @swagger_auto_schema(
        operation_description="Создать новое событие в календаре пользователя",
        request_body=GoogleCalendarEventSerializer,
        responses={
            200: GoogleCalendarEventSerializer,
            400: openapi.Response('Ошибка в данных события'),
        }
    )
    def post(self, request, *args, **kwargs):
        '''Создать новое событие в календаре пользователя'''
        calendar_id = request.data.get('calendar_id')
        event_data = request.data.get('event_data')

        if not calendar_id or not event_data:
            return Response({"error": "Параметры calendar_id и event_data обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        calendar_service = GoogleCalendarService()
        event = calendar_service.create_event(request.user, calendar_id, event_data)
        serializer = GoogleCalendarEventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Обновить событие в календаре пользователя",
        request_body=GoogleCalendarEventSerializer,
        responses={
            200: GoogleCalendarEventSerializer,
            400: openapi.Response('Ошибка в данных события')
        }
    )
    def put(self, request, *args, **kwargs):
        '''Обновить событие в календаре пользователя'''
        calendar_id = request.data.get('calendar_id')
        event_id = request.data.get('event_id')
        event_data = request.data.get('event_data')

        if not calendar_id or not event_id or not event_data:
            return Response({"error": "Параметры calendar_id, event_id и event_data обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        calendar_service = GoogleCalendarService()
        event = calendar_service.update_event(request.user, calendar_id, event_id, event_data)
        serializer = GoogleCalendarEventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Удалить событие из календаря пользователя",
        responses={
            200: openapi.Response('Событие успешно удалено'),
            400: openapi.Response('Ошибка в параметрах'),
        }
    )
    def delete(self, request, *args, **kwargs):
        calendar_id = request.data.get('calendar_id')
        event_id = request.data.get('event_id')

        if not calendar_id or not event_id:
            return Response({"error": "Параметры calendar_id и event_id обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        calendar_service = GoogleCalendarService()
        calendar_service.delete_event(request.user, calendar_id, event_id)
        return Response({"success": "Событие успешно удалено"}, status=status.HTTP_200_OK)


class UserCalendarListApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить список календарей пользователя",
        responses={
            200: UserCalendarSerializer(many=True),
            404: openapi.Response('Календари не найдены', examples={
                'application/json': {"error": "У пользователя нет календарей"}
            }),
            500: openapi.Response('Ошибка сервера')
        }
    )
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

    @swagger_auto_schema(
        operation_description="Обновить список календарей пользователя",
        responses={
            200: UserCalendarSerializer(many=True),
            500: openapi.Response('Ошибка сервера')
        }
    )
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

    @swagger_auto_schema(    
        operation_description="Переключить активный календарь пользователя",
        manual_parameters=[
            openapi.Parameter('calendar_id', openapi.IN_QUERY, description='ID календаря', type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response('Календарь успешно переключен', examples={
                'application/json': {"success": "Календарь успешно переключен"}
            })
        }
    )
    def post(self, request, *args, **kwargs):
        calendar_id = request.data.get('calendar_id')
        calendar_service = GoogleCalendarService()
        calendar_service.toggle_calendar_select(request.user, calendar_id)
        return Response({"success": "Календарь успешно переключен"}, status=status.HTTP_200_OK)