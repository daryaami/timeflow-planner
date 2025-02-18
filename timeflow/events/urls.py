from django.urls import path
from .apis import UserCalendarsEventsApi, GoogleCalendarsListApi

urlpatterns = [
    path('all/', UserCalendarsEventsApi.as_view(), name='calendar_events'),
    path('calendars/', GoogleCalendarsListApi.as_view(), name='google_calendars_list')
]