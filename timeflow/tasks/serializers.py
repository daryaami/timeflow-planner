from rest_framework import serializers
from .models import Task, TimeLog, Category
from events.models import UserCalendar
from django.db.models import Q


class TimeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLog
        fields = [
            'id',
            'start_time',
            'end_time',
            'created_at',
            'updated_at',
            'google_event_id'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color', 'is_default']


class TaskSerializer(serializers.ModelSerializer):
    time_logs = TimeLogSerializer(many=True, read_only=True)
    calendar = serializers.PrimaryKeyRelatedField(
        queryset=UserCalendar.objects.all(),
        required=False
    )

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'priority',
            'category',
            'duration',
            'due_date',
            'calendar',
            'completed',
            'created_at',
            'updated_at',
            'time_logs',
            'notes',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user

        if 'calendar' not in validated_data:
            try:
                validated_data['calendar'] = user.calendars.get(primary=True)
            except UserCalendar.DoesNotExist:
                raise serializers.ValidationError("У пользователя нет основного календаря.")

        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('user', None)
        return super().update(instance, validated_data)
    

from rest_framework import serializers
from tasks.models import Task, TimeLog

class EventFromTaskSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    calendar_id = serializers.IntegerField()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()

    def validate(self, data):
        if data['end'] <= data['start']:
            raise serializers.ValidationError("Дата окончания должна быть позже даты начала")
        return data
