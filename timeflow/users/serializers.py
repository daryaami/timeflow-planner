from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'google_id',
            'name',
            'picture',
            'joined_on',
            'time_zone',
            'is_active',
            'is_staff',
        ]
        read_only_fields = ['id', 'joined_on', 'is_staff', 'is_active']