from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class UserCalendar(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="calendars"
    )
    calendar_id = models.CharField(
        max_length=255,
        help_text="Идентификатор календаря из Google.",
        primary_key=True
    )
    summary = models.CharField(
        max_length=255,
        help_text="Название календаря, как отображается у пользователя."
    )
    description = models.TextField(
        blank=True, 
        null=True,
        help_text="Описание календаря, если доступно."
    )
    owner = models.BooleanField(
        blank=True,
        default=True,
        help_text='Является ли пользователь владельцем календаря.'
    )
    background_color = models.CharField(
        max_length=7, 
        blank=True, 
        null=True,
        help_text="Цвет календаря в формате HEX (например, #ff0000)."
    )
    selected = models.BooleanField(
        default=True,
        help_text="Флаг, указывающий выбран ли календарь для отображения."
    )
    time_zone = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="Часовой пояс календаря."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    primary = models.BooleanField(default=False, help_text="Флаг, указывающий является ли основным календарем.")

    class Meta:
        unique_together = ("user", "calendar_id")
        verbose_name = "Календарь пользователя"
        verbose_name_plural = "Календари пользователей"

    def __str__(self):
        return f"{self.summary} ({self.calendar_id})"
