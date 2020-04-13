from rest_framework import serializers
from gpt2.models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):

    chat = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'body', 'created', 'chat', 'sender_name']
        read_only_fields = ['created', 'sender_name']


class ChatPreviewSerializer(serializers.ModelSerializer):

    messages_count = serializers.SerializerMethodField()
    last_message_sent_at = serializers.SerializerMethodField()

    def get_messages_count(self, obj):
        return obj.messages.count()

    def get_last_message_sent_at(self, obj):
        if obj.messages.exists():
            return obj.messages.last().created
        else:
            return None

    class Meta:
        model = Chat
        fields = ['id', 'name', 'created', 'messages_count',
                  'last_message_sent_at']


class ChatDetailsSerializer(serializers.ModelSerializer):

    messages = MessageSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'name', 'created', 'messages']
        read_only_fields = ['created']

    def create(self, validated_data):
        return Chat(**validated_data)
