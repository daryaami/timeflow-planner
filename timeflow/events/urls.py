from django.urls import path
from .apis import UserCalendarEventsApi, UserCalendarListApi, ToggleUserCalendarSelectApi, UpdateUserCalendarApi

urlpatterns = [
    path('', UserCalendarEventsApi.as_view(), name='calendar_events'),
    path('calendars/', UserCalendarListApi.as_view(), name='google_calendars_list'),
    path('calendars/toggle_select/', ToggleUserCalendarSelectApi.as_view(), name='toggle_calendar_select'),
    path('calendars/update/', UpdateUserCalendarApi.as_view(), name='update_calendar'),
]