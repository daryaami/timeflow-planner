
from django.urls import path

from .apis import GoogleLoginRedirectApi, GoogleLoginApi, AccessTokenApi

app_name = 'google_auth'

urlpatterns = [
    path('', GoogleLoginRedirectApi.as_view(), name='google_auth'),
    path('callback/', GoogleLoginApi.as_view(), name='google_callback'),

    path('access/', AccessTokenApi.as_view(), name='google_access'),
]
