from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    # username -> str
    sender = serializers.StringRelatedField

    class Meta:
        model = Message
        fields = ["id", "sender", "content", "timestamp"]