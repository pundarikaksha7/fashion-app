from rest_framework import serializers
from .models import DirectMessage

class DirectMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectMessage
        fields = ['id', 'sender', 'recipient', 'message', 'timestamp', 'is_read']