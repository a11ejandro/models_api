from django.apps import AppConfig

class Gpt2Config(AppConfig):

    name = 'gpt2'

    def ready(self):
        import gpt2.signals
