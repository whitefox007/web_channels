from rest_framework import serializers
from chat.models import Chat

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('sender', 'message', 'thread_name', 'timestamp')