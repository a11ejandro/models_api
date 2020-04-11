from .models import Chat, Message
from django.forms import ModelForm


class ChatForm(ModelForm):

    class Meta:
        model = Chat
        fields = ['name', 'user']

class MessageForm(ModelForm):

    class Meta:
        model = Message
        fields = ['body', 'chat', 'sender_name']
