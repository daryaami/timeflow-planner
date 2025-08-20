from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from events.services import GoogleCalendarService
from core.exceptions import GoogleAuthError, GoogleNetworkError
from .models import UserCalendar
from events.serializers import GoogleCalendarEventSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction

from .models import Task, Category, TimeLog
from .serializers import EventFromTaskSerializer, TaskSerializer, CategorySerializer, TimeLogSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Task.objects.none()
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Category.objects.none()
        return Category.objects.filter(
            Q(user=self.request.user) | Q(is_default=True)
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TimeLogViewSet(viewsets.ModelViewSet):
    serializer_class = TimeLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return TimeLog.objects.none()
        return TimeLog.objects.filter(task__user=user)

    def perform_create(self, serializer):
        task = serializer.validated_data['task']
        if task.user != self.request.user:
            raise PermissionDenied("Вы не можете добавлять логи к чужим задачам.")
        serializer.save()

class CreateEventFromTaskApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Создать событие и timelog на основе задачи",
        manual_parameters=[
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
        user_calendar = get_object_or_404(UserCalendar, calendar_id=validated['calendar_id'], user=request.user)

        event_data = {
            "summary": task.title,
            "start": {"dateTime": validated["start"].isoformat()},
            "end": {"dateTime": validated["end"].isoformat()},
        }

        gcal_service = GoogleCalendarService()

        calendar_event = gcal_service.create_event(
            user=request.user,
            calendar_id=user_calendar.calendar_id,
            event_data=event_data
        )

        timelog = TimeLog.objects.create(
            user=request.user,
            task=task,
            start_time=validated["start"],
            end_time=validated["end"],
            google_event_id=calendar_event["id"]
        )




