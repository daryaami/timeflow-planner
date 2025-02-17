from django.urls import path
from .apis import RefreshTokenView, LogoutView


urlpatterns = [
    path("refresh/", RefreshTokenView.as_view(), name="token_refresh"),
    path('logout/', LogoutView.as_view(), name='logout'),
]