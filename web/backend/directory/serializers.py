from rest_framework import serializers

class FileSerializer(serializers.Serializer):
    name = serializers.CharField()
    path = serializers.CharField()