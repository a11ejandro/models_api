from django.conf import settings
from django.http import HttpResponse
import urllib
import json


class Gpt2():
    # accepted args are:
    # 'text', 'quiet', 'nsamples', 'unconditional', 'batch_size', 'length', 'temperature', 'top_k'

    @staticmethod
    def request(**kwargs):
        # It is supposed that no auth is necessary
        response = urllib.request.urlopen(settings.GPT2_ENDPOINT, data=kwargs)
        return response.read()


class Gpt2Chat():
    LAST_MESSAGES_COUNT = 100
    LIMIT_MESSAGE_LENGTH = 300

    def __init__(self, chat):
        self.chat = chat

    def uncomplete_dialog(self):
        # Pass last N messages of dialog to GPT, predict N + 1.
        last_n = self.chat.messages.all().order_by('-id')[:self.LAST_MESSAGES_COUNT]
        result = ''

        for message in last_n:
            # structure replies as a regular dialog, e.g:
            # - How do you do?
            # - Fine, how are you?
            result += '- ' + message.body + '\n'

        # -  Placeholder for gpt2 reply
        result += '- '
        return result

    def truncated_response(self, response):
        sentences = response.split('. ')
        
        if len(sentences) == 0:
            return sentences
        else:
            return ". ".join(sentences)

    def next_message(self):
        concatenated = self.uncomplete_dialog()
        data = {'text': concatenated, 'unconditional': False, 'length': self.LIMIT_MESSAGE_LENGTH}
        response = Gpt2.request(**data)

        return self.truncated_response(response)



        

    

