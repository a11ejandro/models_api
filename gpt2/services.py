from django.db import transaction
from .models import Message
from .requests import Gpt2Chat
from .serializers import MessageSerializer


def post_and_reply(data, chat, user):
    serializer = MessageSerializer(data=data)

    if serializer.is_valid():
        try:
            with transaction.atomic():
                serializer.save(sender_name=user.first_name or "Nobody")
                reply_body = Gpt2Chat(chat).next_message()
                new_reply = Message(
                    chat=chat, body=reply_body, sender_name='GPT2')
                new_reply.save()

                return (True, None)

        except Exception as e:
            return (False, [str(e)])

    else:
        return (False, serializer.errors)
