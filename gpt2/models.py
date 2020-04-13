from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):

    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Message(models.Model):

    chat = models.ForeignKey(
        Chat, related_name='messages', on_delete=models.CASCADE)
    sender_name = models.CharField(max_length=200, default='Nobody')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    get_latest_by = 'created'
