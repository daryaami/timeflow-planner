from rest_framework import serializers
from .models import UserCalendar

class UserCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCalendar
        fields = [
            'id', 'user', 'calendar_id', 'summary', 'description', 'owner',
            'background_color', 'selected', 'created_at', 'updated_at', 'time_zone'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']