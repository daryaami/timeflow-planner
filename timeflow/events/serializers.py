from rest_framework import serializers
from .models import UserCalendar

class UserCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCalendar
        fields = [
            'user', 'calendar_id', 'summary', 'description', 'owner',
            'background_color', 'selected', 'created_at', 'updated_at', 'time_zone', 'primary'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']


class GoogleCalendarEventSerializer(serializers.Serializer):
    id = serializers.CharField()
    summary = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(required=False)
    htmlLink = serializers.URLField(required=False)
    created = serializers.DateTimeField(required=False)
    updated = serializers.DateTimeField(required=False)
    # Вложенные поля старт/энд будем принимать в виде словаря, а затем преобразовывать их
    start = serializers.DictField(required=False)
    end = serializers.DictField(required=False)
    # Можно сохранять email организатора как строку (если важен только email)
    organizer_email = serializers.SerializerMethodField()
    calendar = serializers.CharField(required=False)

    def get_organizer_email(self, obj):
        organizer = obj.get('organizer')
        if isinstance(organizer, dict):
            return organizer.get('email')
        return None

    def to_representation(self, instance):
        """
        Здесь мы можем управлять видом итогового объекта:
         - Извлечь значение dateTime из полей start и end,
         - При необходимости преобразовать формат даты.
        """
        representation = super().to_representation(instance)
        
        # Преобразуем поля start и end: выбираем dateTime, если оно есть, иначе date.
        for time_field in ('start', 'end'):
            time_data = instance.get(time_field, {})
            if isinstance(time_data, dict):
                # Приоритет: dateTime -> date
                representation[time_field] = time_data.get('dateTime') or time_data.get('date')
            else:
                representation[time_field] = time_data

        return representation