from django.contrib.auth.models import User
from rest_framework import serializers

from app.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            'id',
            'upload_datetime',
            'number_of_pages',
            'size',
        )


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class SearchSerializer(serializers.Serializer):
    keyword = serializers.CharField()


class OccurrencesSerializer(serializers.Serializer):
    keyword = serializers.CharField()


class TopSerializer(serializers.Serializer):
    count = serializers.IntegerField(min_value=1, default=5, required=False)


class SummarySerializer(serializers.Serializer):
    count = serializers.IntegerField(min_value=1, default=None, required=False)
