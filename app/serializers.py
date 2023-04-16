from rest_framework import serializers
from models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'id',
            'upload_datetime',
            'number_of_pages',
            'size',
        ]


class SearchSerializer(serializers.Serializer):
    keyword = serializers.CharField()


class OccurrencesSerializer(serializers.Serializer):
    keyword = serializers.CharField()


class TopSerializer(serializers.Serializer):
    count = serializers.IntegerField(min_value=1, default=5, required=False)
