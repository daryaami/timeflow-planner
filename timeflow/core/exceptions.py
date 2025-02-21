from rest_framework.exceptions import APIException
from rest_framework import status


class UserNotFoundError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Пользователь не найден."
    default_code = "user_not_found"


class GoogleAuthError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Ошибка авторизации через Google."
    default_code = "google_auth_error"


class InvalidGoogleResponseError(APIException):
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = "Некорректный ответ от сервиса Google."
    default_code = "invalid_google_response"


class InvalidGoogleTokenError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Неверный или устаревший токен."
    default_code = "invalid_google_token"


class ExpiredRefreshTokenError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Google Refresh-токен истёк, требуется повторный запрос разрешений."
    default_code = "expired_google_refresh_token"


class RefreshTokenError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Не удалось обновить токен."
    default_code = "refresh_token_error"


class ReauthRequiredError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "JWT Refresh-токен истёк, требуется повторная авторизация."
    default_code = "reauth_required"


class GoogleTokenExchangeError(APIException):
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = "Не удалось обменять код авторизации на токены."
    default_code = "google_token_exchange_error"


class InvalidStateError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Ошибка проверки state параметра. Возможна CSRF-атака."
    default_code = "invalid_state"


class GoogleNetworkError(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Ошибка соединения с Google."
    default_code = "google_network_error"

class GoogleCalendarError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Ошибка при работе с Google Календарём."
    default_code = "google_calendar_error"

class GoogleNetworkError(APIException):
    status_code = 503  # HTTP 503 Service Unavailable, потому что ошибка связана с внешним сервисом
    default_detail = 'Произошла ошибка при обращении к Google API.'
    default_code = 'google_api_error'

class CalendarSyncError(APIException):
    status_code = 500  # HTTP 500 Internal Server Error, ошибка на сервере
    default_detail = 'Ошибка синхронизации календаря пользователя.'
    default_code = 'calendar_sync_error'

class CalendarCreationError(APIException):
    status_code = 400  # HTTP 400 Bad Request, ошибка на уровне данных
    default_detail = 'Ошибка при создании календаря пользователя.'
    default_code = 'calendar_creation_error'