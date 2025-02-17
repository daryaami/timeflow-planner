from rest_framework import serializers

class GoogleAccessTokensSerializer(serializers.Serializer):
    id_token = serializers.CharField()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField(required=False, allow_null=True)