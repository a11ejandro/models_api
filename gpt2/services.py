from django.db import transaction
from .models import Message, Chat
from .requests import Gpt2Chat
from .serializers import MessageSerializer


def post_and_reply(data, chat, user):
    serializer = MessageSerializer(data=data)

    if serializer.is_valid():
        try:
            with transaction.atomic:
                serializer.save(sender_name=request.user.first_name)
                reply_body = Gpt2Chat.next_message(chat)
                new_reply = Message(chat=chat, body=reply_body, sender_name='GPT2')
                new_reply.save()

                return (True, None)

        except:
            return (False, ["Something went wrong"])
    
    else:
        return (False, serializer.errors)
