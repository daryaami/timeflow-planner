from django.urls import path
from .apis import CreateEventFromTaskApi, UserCalendarEventsApi, UserCalendarListApi, ToggleUserCalendarSelectApi, UpdateUserCalendarApi

urlpatterns = [
    path('create-from-task/', CreateEventFromTaskApi.as_view(), name='create_event_from_task'),
    path('', UserCalendarEventsApi.as_view(), name='calendar_events'),
    path('calendars/', UserCalendarListApi.as_view(), name='google_calendars_list'),
    path('calendars/toggle-select/', ToggleUserCalendarSelectApi.as_view(), name='toggle_calendar_select'),
    path('calendars/update/', UpdateUserCalendarApi.as_view(), name='update_calendar'),
]