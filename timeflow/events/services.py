# events/services.py

from django.conf import settings
import requests
from google_auth.services import get_user_credentials
from core.exceptions import GoogleNetworkError
from .models import UserCalendar
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


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
            print('Сервис получен')
            calendar_list = service.calendarList().list().execute()
            print('Список календарей получен: ', calendar_list)
            
            return [
            {
                "id": calendar.get("id"),
                "summary": calendar.get("summary"),
                "description": calendar.get("description", None),
                "timeZone": calendar.get("timeZone", None),
                "primary": calendar.get("primary", 'false'),
                'backgroundColor': calendar.get("backgroundColor"),
                # 'foregroundColor': calendar.get("foregroundColor"),
                "owner": calendar.get("accessRole", False) == 'owner',
            }
            for calendar in calendar_list.get("items", [])
            ]

        except HttpError as e:
            raise GoogleNetworkError(f"Google API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")

    def get_events_from_calendar(self, calendar):
        """
        Получает события для заданного календаря.
        calendar: экземпляр модели UserCalendar.
        """
        user = calendar.user
        access_token = self._get_credentials(user).token
        print('Токен получен успешно')
        headers = self._get_headers(access_token)
        url = self.CALENDAR_EVENTS_URL.format(calendar_id=calendar.calendar_id)
        response = requests.get(url, headers=headers)
        
        if not response.ok:
            raise GoogleNetworkError(f"Не удалось получить события для календаря {calendar.calendar_id}.")
        
        try:
            data = response.json()
        except ValueError:
            raise GoogleNetworkError(f"Не удалось распарсить ответ для календаря {calendar.calendar_id}.")
        
        return data

    def get_all_events(self, user):
        """
        Получает события для всех выбранных календарей пользователя.
        Возвращает список событий, где каждое событие дополнено информацией о календаре.
        """
        # Получаем календари, выбранные для отображения
        user_calendars = UserCalendar.objects.filter(user=user, selected=True)
        events_list = []
        for calendar in user_calendars:
            try:
                calendar_events = self.get_events_from_calendar(calendar)
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
