from django.conf import settings
from django.http import HttpResponse
import urllib
import json


class Gpt2():
    # accepted args are:
    # 'text', 'quiet', 'nsamples', 'unconditional', 'batch_size', 'length', 'temperature', 'top_k'

    @staticmethod
    def request(self, **kargs):
        # It is supposed that no auth is necessary
        response = urllib.request.urlopen(settings.GPT2_ENDPOINT, data=kargs)
        response.read()


class Gpt2Chat():

    def __init__(self, chat):
        self.chat = chat

    def concatenated_messages(self):
        # Pass last 100 messages of dialog to GPT, predict 101st.
        last_100 = self.chat.messages.objects().order_by('-id')[:100]

        result = ''
        for message in last_100:
            # structure replies as a regular dialog, e.g:
            # - How do you do?
            # - Fine, how are you?
            result += '\n- ' + message.body

        result += '\n- '  # Placeholder for GPT-2 answer

        return result

    def next_message(self):
        concatenated = self.concatenated_messages()
        data = {'text': concatenated, 'unconditional': False, 'length': 300}
        response = Gpt2.request(**data)
        return response.read



        

    

