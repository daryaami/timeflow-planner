from django.urls import path
from .apis import UserCalendarsEventsApi, UserCalendarsListApi, UpdateUserCalendarApi

urlpatterns = [
    path('all/', UserCalendarsEventsApi.as_view(), name='calendar_events'),
    path('calendars/', UserCalendarsListApi.as_view(), name='google_calendars_list'),
    path('refresh_calendars/', UpdateUserCalendarApi.as_view(), name='update_calendar'),
]