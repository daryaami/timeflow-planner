from django.urls import path
from .apis import CustomJwtRefreshView, LogoutView


urlpatterns = [
    path('refresh/', CustomJwtRefreshView.as_view(), name='jwt_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]