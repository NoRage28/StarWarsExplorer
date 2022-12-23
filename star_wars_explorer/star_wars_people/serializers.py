from rest_framework import serializers
from .models import Dataset


class DatasetViewSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Dataset
        fields = ['name']
