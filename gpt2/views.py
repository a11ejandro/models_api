from django.shortcuts import get_object_or_404
from django.db.models import Count, Max

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Chat, Message
from .serializers import ChatDetailsSerializer, ChatPreviewSerializer
from .services import post_and_reply


class ChatViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Chat.objects.all()

    # Can list chats of other users
    def list(self, request):
        annotated = self.queryset.annotate(
            last_message_created=Max('messages__created'),
            messages_count=Count('messages')
        )

        serializer = ChatPreviewSerializer(annotated, many=True)
        return Response(serializer.data)

    # Can see details of chat of other user
    def retrieve(self, request, pk=None):
        chat = get_object_or_404(self.queryset, pk=pk)
        serializer = ChatDetailsSerializer(chat)
        return Response(serializer.data)

    def create(self, request):
        serializer = ChatDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        else:
            return Response({'errors': serializer.errors})


class MessageViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()

    def create(self, request):
        chats = Chat.objects.all()
        chat = get_object_or_404(chats, pk=request.data.get('chat'))

        if chat.user_id != request.user.id:
            return Response({'errors': 'Chat not available for posting'},
                            status=status.HTTP_403_FORBIDDEN)

        success, error = post_and_reply(
            data=request.data, chat=chat, user=request.user)

        if success:
            chat_serializer = ChatDetailsSerializer(chat)
            return Response(chat_serializer.data)
        else:
            return Response({'errors': error},
                            status=status.HTTP_400_BAD_REQUEST)
