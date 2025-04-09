from django.urls import path
from .apis import UserCalendarsEventsApi, UserCalendarsListApi, ToggleUserCalendarSelectApi, UpdateUserCalendarApi

urlpatterns = [
    path('all/', UserCalendarsEventsApi.as_view(), name='calendar_events'),
    path('calendars/', UserCalendarsListApi.as_view(), name='google_calendars_list'),
    path('calendars/toggle_select/', ToggleUserCalendarSelectApi.as_view(), name='toggle_calendar_select'),
    path('calendars/update/', UpdateUserCalendarApi.as_view(), name='update_calendar'),
]