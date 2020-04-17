from django.contrib.auth.models import User

from rest_framework import serializers
from gpt2.models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):

    chat = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'body', 'created', 'chat', 'sender_name']
        read_only_fields = ['created', 'sender_name']


class ChatPreviewSerializer(serializers.ModelSerializer):
    messages_count = serializers.IntegerField()
    last_message_sent_at = serializers.SerializerMethodField()

    def get_last_message_sent_at(self, obj):
        if hasattr(obj, 'last_message_created'):
            return obj.last_message_created
        elif obj.messages.exists():
            obj.messages.last().created
        else:
            return None

    def get_messages_count(self, obj):
        if hasattr(obj, 'messages_count'):
            return obj.messages_count
        else:
            return obj.messages.count()

    class Meta:
        model = Chat
        fields = ['id', 'name', 'created', 'messages_count',
          'last_message_sent_at']


class ChatDetailsSerializer(serializers.ModelSerializer):

    messages = MessageSerializer(many=True, required=False, read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                              required=False)

    class Meta:
        model = Chat
        fields = ['id', 'name', 'created', 'messages', 'user']
        read_only_fields = ['created']
