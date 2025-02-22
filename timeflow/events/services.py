# events/services.py

from django.conf import settings
import requests
from rest_framework import serializers
from google_auth.services import get_user_credentials
from core.exceptions import GoogleNetworkError
from .models import UserCalendar
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .serializers import UserCalendarSerializer
import logging
from django.db import transaction
from core.exceptions import CalendarCreationError, CalendarSyncError

logger = logging.getLogger(__name__)


class GoogleCalendarService:
    CALENDAR_EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

    def _get_credentials(self, user):
        return get_user_credentials(user.google_id)

    def _build_google_service(self, user):
        credentials = self._get_credentials(user)
        service = build('calendar', 'v3', credentials=credentials)
        return service

    def _get_headers(self, access_token):
        """
        Формируем заголовки для запроса с переданным access_token.
        """
        return {
            "Authorization": f"Bearer {access_token}",
        }

    def get_google_calendars(self, user):
        """
        Получает список календарей, доступных для пользователя.
        Возвращает список словарей, содержащих информацию о календарях,
        включая id, summary, description, timezone и primary.
        
        :param user: пользователь, для которого нужно получить список календарей
        :raises GoogleNetworkError: если возникла ошибка при работе с Google API
        :raises Exception: если возникла любая другая ошибка
        """
        try:
            service = self._build_google_service(user)
            calendar_list = service.calendarList().list().execute()
            
            return [
            {
                "calendar_id": calendar.get("id"),
                "summary": calendar.get("summary"),
                "description": calendar.get("description", None),
                "time_zone": calendar.get("timeZone", None),
                "primary": calendar.get("primary", 'false'),
                'background_color': calendar.get("backgroundColor"),
                # 'foregroundColor': calendar.get("foregroundColor"),
                "owner": calendar.get("accessRole", False) == 'owner',
            }
            for calendar in calendar_list.get("items", [])
            ]

        except HttpError as e:
            raise GoogleNetworkError(f"Ошибка при обращении к Google API: {str(e)}")
        except Exception as e:
            raise GoogleNetworkError(f"Непредвиденная ошибка при получении календарей: {str(e)}")

    def create_user_calendars(self, user):
        """
        Создает календари пользователя в базе данных.
        """
        try:
            calendars = self.get_google_calendars(user)
            serializer = UserCalendarSerializer(data=calendars, many=True)
            if serializer.is_valid():
                user_calendars = [UserCalendar(**data, user=user) for data in serializer.validated_data]
                UserCalendar.objects.bulk_create(user_calendars)
            else:
                raise CalendarCreationError(f"Ошибка сериализации календарей: {serializer.errors}")
        except CalendarSyncError as e:
            raise CalendarSyncError(f"Ошибка синхронизации календарей для пользователя {user}: {e}")
        except Exception as e:
            raise CalendarCreationError(f"Ошибка при создании календарей для пользователя {user}: {str(e)}")

    def get_events_from_calendar(self, calendar, credentials):
        """
        Получает события из календаря пользователя.
        """
        try:
            access_token = credentials.token
            headers = self._get_headers(access_token)
            url = self.CALENDAR_EVENTS_URL.format(calendar_id=calendar.calendar_id)
            response = requests.get(url, headers=headers)

            if not response.ok:
                raise GoogleNetworkError(f"Ошибка при получении событий: {response.status_code}")

            return response.json()
        except GoogleNetworkError as e:
            raise GoogleNetworkError(f"Ошибка при получении событий из календаря {calendar.calendar_id}: {str(e)}")
        except Exception as e:
            raise CalendarSyncError(f"Неизвестная ошибка при получении событий из календаря {calendar.calendar_id}: {str(e)}")

    def get_all_events(self, user):
        """
        Получает события для всех выбранных календарей пользователя.
        Возвращает список событий, где каждое событие дополнено информацией о календаре.
        """
        # Получаем календари, выбранные для отображения
        user_calendars = UserCalendar.objects.filter(user=user, selected=True)
        events_list = []
        credentials = self._get_credentials(user)
        for calendar in user_calendars:
            try:
                calendar_events = self.get_events_from_calendar(calendar, credentials)
                # Предполагаем, что в ответе содержится ключ "items" с событиями
                events = calendar_events.get("items", [])
                events_list.extend(events)
            except Exception as e:
                # Можно логировать ошибки получения событий для конкретного календаря
                # Или вернуть специальный результат для этого календаря
                events_list.append({
                    "error": str(e),
                    "calendar": {
                        "calendar_id": calendar.calendar_id,
                        "name": calendar.name,
                    }
                })
        return events_list

    def toggle_calendar_select(self, user, calendar_id):
        """
        Переключает выбор календарей для пользователя.
        """
        try:
            calendar = UserCalendar.objects.get(user=user, calendar_id=calendar_id)
            calendar.selected = not calendar.selected
            calendar.save()
        except UserCalendar.DoesNotExist:
            raise CalendarSyncError(f"Календарь {calendar_id} не найден")
