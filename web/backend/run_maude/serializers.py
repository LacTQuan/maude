from rest_framework import serializers

class MaudeSerializer(serializers.Serializer):
    name = serializers.CharField()
    path = serializers.CharField()