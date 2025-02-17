from django.urls import path
from .apis import CalendarEventsApi

urlpatterns = [
    path('events/', CalendarEventsApi.as_view(), name='calendar_events'),
]