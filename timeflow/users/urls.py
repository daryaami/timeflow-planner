from django.urls import path
from .apis import RefreshJWTView, LogoutView


urlpatterns = [
    path("refresh/", RefreshJWTView.as_view(), name="token_refresh"),
    path('logout/', LogoutView.as_view(), name='logout'),
]