from rest_framework import serializers
from .models import UserCalendar

class UserCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCalendar
        fields = [
            'id',
            'user', 'calendar_id', 'summary', 'description', 'owner',
            'background_color', 'selected', 'created_at', 'updated_at', 'time_zone', 'primary'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


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
    description = serializers.CharField(required=False, allow_blank=True)
    
    extendedProperties = serializers.DictField(required=False)

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
    

class GoogleCalendarEventCreateSerializer(serializers.Serializer):
    summary = serializers.CharField(required=True)  # название события
    calendar_id = serializers.IntegerField(required=True)
    description = serializers.CharField(required=False, allow_blank=True)

    # start/end принимаем в виде словаря с ключом dateTime или date
    start = serializers.DictField(required=True)
    end = serializers.DictField(required=True)

    def validate(self, data):
        """
        Проверяем что start/end есть и имеют правильный формат
        """
        for field in ("start", "end"):
            time_data = data.get(field, {})
            if not isinstance(time_data, dict):
                raise serializers.ValidationError({field: "Ожидается словарь"})
            if not (time_data.get("dateTime") or time_data.get("date")):
                raise serializers.ValidationError({
                    field: "Нужно указать либо dateTime, либо date"
                })
        return data
    
class GoogleCalendarEventUpdateSerializer(GoogleCalendarEventCreateSerializer):
    event_id = serializers.CharField(required=True)
    calendar_id = serializers.IntegerField(required=True)
    extendedProperties = serializers.DictField(required=False)
    summary = serializers.CharField(required=False)

class GoogleCalendarEventDeleteSerializer(serializers.Serializer):
    event_id = serializers.CharField(required=True)
    calendar_id = serializers.IntegerField(required=True)

class EventFromTaskSerializer(serializers.Serializer):
    task_id = serializers.IntegerField(required=True)
    calendar_id = serializers.IntegerField(required=True)
    start = serializers.DateTimeField(required=True)
    end = serializers.DateTimeField(required=True)

    def validate(self, data):
        if data['end'] <= data['start']:
            raise serializers.ValidationError("Дата окончания должна быть позже даты начала")
        return data

    
# class EventFromTaskUpdateSerializer(EventFromTaskSerializer):
#     event_id = serializers.IntegerField(required=True)
#     task_id = serializers.IntegerField(required=True)
#     timelog_id = serializers.IntegerField(required=True)
#     calendar_id = serializers.IntegerField(required=True)
    
#     summary = serializers.CharField(required=False)
#     start = serializers.DateTimeField(required=False)
#     end = serializers.DateTimeField(required=False)




