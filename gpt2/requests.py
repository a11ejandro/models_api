from django.conf import settings
import urllib


class Gpt2():
    # accepted args are:
    # 'text', 'quiet', 'nsamples', 'unconditional', 'batch_size',
    # 'length', 'temperature', 'top_k'

    @staticmethod
    def request(**kwargs):
        # It is supposed that no auth is necessary
        data = bytes(urllib.parse.urlencode(kwargs), encoding='utf8')
        response = urllib.request.urlopen(settings.GPT2_ENDPOINT, data=data)
        return response.read().decode('utf-8')


class Gpt2Chat(Gpt2):
    LAST_MESSAGES_COUNT = 100
    LIMIT_MESSAGE_LENGTH = 300

    def __init__(self, chat):
        self.chat = chat

    def uncomplete_dialog(self):
        # Pass last N messages of dialog to GPT, predict N + 1.
        last_n = self.chat.messages.all().order_by(
            '-id')[:self.LAST_MESSAGES_COUNT][::-1]
        result = ''

        for message in last_n:
            # structure replies as a regular dialog, e.g:
            # - How do you do? - Fine, how are you?
            result += '- ' + message.body + ' '

        # -  Placeholder for gpt2 reply
        result += '- '
        return result

    def truncated_response(self, response):
        # GPT2 may  predict more than one answer, we need only the first one
        replies = response.split('- ')
        replies = list(filter(lambda str: len(str) > 3, replies))
        sentences = replies[0].split('. ')

        if len(sentences) == 0:
            return sentences
        else:
            return ". ".join(sentences)

    def next_message(self):
        concatenated = self.uncomplete_dialog()
        data = {'text': concatenated, 'unconditional': False,
                'length': self.LIMIT_MESSAGE_LENGTH}

        response = self.request(**data)

        return self.truncated_response(response)
