# events/api.py
from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from tasks.models import Task, TimeLog
from .services import GoogleCalendarService, add_event_extended_properties
from core.exceptions import GoogleAuthError, GoogleNetworkError
from .models import UserCalendar
from .serializers import EventFromTaskSerializer, GoogleCalendarEventCreateSerializer, GoogleCalendarEventDeleteSerializer, GoogleCalendarEventSerializer, GoogleCalendarEventUpdateSerializer, UserCalendarSerializer
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
        except GoogleNetworkError as e:
            raise e
        except Exception as e:
            raise GoogleAuthError(detail=str(e))
        
    @swagger_auto_schema(
        operation_description="Создать новое событие в календаре пользователя",
        request_body=GoogleCalendarEventCreateSerializer,
        responses={
            201: GoogleCalendarEventSerializer,
            400: openapi.Response('Ошибка в данных события'),
        }
    )
    def post(self, request, *args, **kwargs):
        '''Создать новое событие в календаре пользователя'''
        # calendar_id = request.data.get('calendar_id')
        # event_data = request.data.get('event_data')

        serializer = GoogleCalendarEventCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        calendar_id = serializer.validated_data.pop("calendar_id")
        event_data = serializer.validated_data

        # if not calendar_id or not event_data:
        #     return Response({"error": "Параметры calendar_id и event_data обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        calendar_service = GoogleCalendarService()
        event = calendar_service.create_event(request.user, calendar_id, event_data)
        
        response_serializer = GoogleCalendarEventSerializer(event)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(
        operation_description="Обновить событие в календаре пользователя",
        request_body=GoogleCalendarEventUpdateSerializer,
        responses={
            200: GoogleCalendarEventSerializer,
            400: openapi.Response('Ошибка в данных события')
        }
    )
    def put(self, request, *args, **kwargs):
        '''Обновить событие в календаре пользователя'''

        serializer = GoogleCalendarEventUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # calendar_id = request.data.get('calendar_id')
        # event_id = request.data.get('event_id')
        # event_data = request.data.get('event_data')

        calendar_id = serializer.validated_data.pop("calendar_id")
        event_id = serializer.validated_data.pop("event_id")
        event_data = serializer.validated_data

        # if not calendar_id or not event_id or not event_data:
        #     return Response({"error": "Параметры calendar_id, event_id и event_data обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        calendar_service = GoogleCalendarService()
        event = calendar_service.update_event(request.user, calendar_id, event_id, event_data)

        response_serializer = GoogleCalendarEventSerializer(event)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Удалить событие из календаря пользователя",
        request_body=GoogleCalendarEventDeleteSerializer,
        responses={
            204: openapi.Response('Событие успешно удалено'),
            400: openapi.Response('Ошибка в параметрах'),
        }
    )
    def delete(self, request, *args, **kwargs):
        # calendar_id = request.data.get('calendar_id')
        # event_id = request.data.get('event_id')

        serializer = GoogleCalendarEventDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        calendar_id = serializer.validated_data["calendar_id"]
        event_id = serializer.validated_data["event_id"]

        # if not calendar_id or not event_id:
        #     return Response({"error": "Параметры calendar_id и event_id обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        calendar_service = GoogleCalendarService()
        calendar_service.delete_event(request.user, calendar_id, event_id)
        
        return Response({"success": "Событие успешно удалено"}, status=status.HTTP_204_NO_CONTENT)


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
    
    
class EventFromTaskApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Создать событие и timelog на основе задачи",
        manual_parameters=[
            openapi.Parameter('task_id', openapi.IN_QUERY, description="ID задачи", type=openapi.TYPE_INTEGER),
            openapi.Parameter('calendar_id', openapi.IN_QUERY, description="ID календаря", type=openapi.TYPE_INTEGER),
            openapi.Parameter('start', openapi.IN_QUERY, description="Дата начала (%Y-%m-%d)", type=openapi.TYPE_STRING),
            openapi.Parameter('end', openapi.IN_QUERY, description="Дата окончания (%Y-%m-%d)", type=openapi.TYPE_STRING),
        ],
        responses={
            201: GoogleCalendarEventSerializer(many=False),
            400: openapi.Response('Неверный формат дат или отсутствуют параметры start и end', examples={
                'application/json': {"error": "Параметры start и end обязательны"}
            }),
            404: openapi.Response('Задача не найдена'),
            500: openapi.Response('Ошибка сервера')
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = EventFromTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        task = get_object_or_404(Task, id=validated['task_id'], user=request.user)
        user_calendar = get_object_or_404(UserCalendar, id=validated['calendar_id'], user=request.user)

        event_data = {
            "summary": task.title,
            "description": task.notes,
            "start": {"dateTime": validated["start"].isoformat()},
            "end": {"dateTime": validated["end"].isoformat()},
        }

        gcal_service = GoogleCalendarService()

        try:
            calendar_event = gcal_service.create_event(
                user=request.user,
                calendar_id=user_calendar.calendar_id,
                event_data=event_data
            )
        except Exception as e:
            return Response({"error": f"Не удалось создать событие в Google Calendar: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            timelog = TimeLog.objects.create(
                # user=request.user,
                task=task,
                start_time=validated["start"],
                end_time=validated["end"],
                google_event_id=calendar_event["id"]
            )
        except Exception as e:
            return Response({"error": f"Не удалось создать timelog: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        extended_event = add_event_extended_properties(calendar_event, task.id, timelog.id)
        response_serializer = GoogleCalendarEventSerializer(extended_event)
    
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(
        operation_description="Обновить событие и timelog",
        manual_parameters=[
            openapi.Parameter('start', openapi.IN_QUERY, description="Дата начала (%Y-%m-%d)", type=openapi.TYPE_STRING),
            openapi.Parameter('end', openapi.IN_QUERY, description="Дата окончания (%Y-%m-%d)", type=openapi.TYPE_STRING),
        ],
        responses={
            200: GoogleCalendarEventSerializer(many=False),
            400: openapi.Response('Неверный формат дат или отсутствуют параметры start и end', examples={
                'application/json': {"error": "Параметры start и end обязательны"}
            }),
            404: openapi.Response('Задача не найдена'),
            500: openapi.Response('Ошибка сервера')
        }
    )
    def put(self, request, *args, **kwargs):
        serializer = GoogleCalendarEventUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        gcal_service = GoogleCalendarService()

        try:
            user_calendar = get_object_or_404(UserCalendar, id=validated["calendar_id"], user=request.user)
        except Exception as e:
            return Response({"error": f"Календарь не найден: {str(e)}"},
                            status=status.HTTP_404_NOT_FOUND)

        event_data = {
            "start": {"dateTime": validated["start"].isoformat()},
            "end": {"dateTime": validated["end"].isoformat()},
        }
        if validated.get("description"):
            event_data["description"] = validated["description"]
        if validated.get("summary"):
            event_data["summary"] = validated["summary"]

        extProps = validated.get("extendedProperties", {}).get("private", {})

        if "timeflow__touched" in extProps and extProps["timeflow__touched"] == True and extProps["timeflow__object-type"] == 1:

            task = get_object_or_404(Task, id=extProps["timeflow__task-id"], user=request.user)
            timelog = get_object_or_404(TimeLog, id=extProps["timeflow__connected-timelog-id"], task=task)

            assert timelog.google_event_id == validated["event_id"], "event_id не совпадает с timelog.google_event_id"
            
            try:
                calendar_event = gcal_service.update_event(request.user, user_calendar.calendar_id, timelog.google_event_id, event_data)
            except Exception as e:
                return Response({"error": f"Не удалось обновить событие в Google Calendar: {str(e)}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            try:
                timelog.start_time = validated["start"]
                timelog.end_time = validated["end"]
                timelog.save()
            except Exception as e:
                return Response({"error": f"Не удалось обновить timelog: {str(e)}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            response_serializer = GoogleCalendarEventSerializer(calendar_event)

            return Response(response_serializer.data, status=status.HTTP_200_OK)

        else:
            try:
                calendar_event = gcal_service.update_event(request.user, user_calendar.calendar_id, validated["event_id"], event_data)
            except Exception as e:
                return Response({"error": f"Не удалось обновить событие в Google Calendar: {str(e)}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            response_serializer = GoogleCalendarEventSerializer(calendar_event)

            return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    def get(self, request, *args, **kwargs):
        return Response({"error": "Метод GET не поддерживается"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    



