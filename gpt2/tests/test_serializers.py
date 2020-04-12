from django.test import TestCase
from datetime import datetime, timedelta
from unittest.mock import patch, PropertyMock
from gpt2.serializers import ChatDetailsSerializer, ChatPreviewSerializer, MessageSerializer
from .factories import ChatFactory, MessageFactory, UserFactory


class TestChatDetailsSerializer(TestCase):
    def setUp(self):
        self.chat = ChatFactory()
        self.chat_message = MessageFactory(chat=self.chat)
        self.other_message = MessageFactory()
        self.serializer = ChatDetailsSerializer(self.chat)


    def testMessages(self):
        self.assertEqual(self.chat_message.id,
            self.serializer.data['messages'][0]['id'])
        self.assertEqual(len(self.serializer.data['messages']), 1)

    def testReadOnlyFields(self):
        created_at = datetime.now() - timedelta(hours = 1)

        data = {
            'id': '300',
            'name': 'Spartans',
            'created': created_at,
            'messages': [{'id': self.chat_message.id}]
        }

        serializer = ChatDetailsSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        new_chat = serializer.save()

        self.assertEqual(new_chat.name, 'Spartans')

        self.assertNotEqual(new_chat.id, 300)
        self.assertNotEqual(new_chat.created, created_at)
        self.assertEqual(new_chat.messages.count(), 0)


class TestChatPreviewSerializer(TestCase):
    def setUp(self):
        self.chat = ChatFactory()
        self.chat_message = MessageFactory(chat=self.chat)
        self.other_message = MessageFactory()
        self.serializer = ChatPreviewSerializer(self.chat)
        

    def testMessagesGetters(self):
        self.assertEqual(self.serializer.data['messages_count'], 1)
        self.assertEqual(self.serializer.data['last_message_sent_at'],
            self.chat_message.created)

class TestMessageSerializer(TestCase):
    def setUp(self):
        self.chat = ChatFactory()

    def testChatRelation(self):
        message = MessageFactory(chat=self.chat)
        serializer = MessageSerializer(message)
        self.assertEqual(serializer.data['chat'], self.chat.id)

    def testReadOnlyFields(self):
        created_at = datetime.now() - timedelta(hours = 1)

        data = {
            'id': 300,
            'body': 'Spartans',
            'created': created_at,
            'chat': self.chat.id,
            'sender_name': 'Toster',
        }

        serializer = MessageSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        new_message = serializer.save()

        self.assertEqual(new_message.body, 'Spartans')
        self.assertEqual(new_message.chat, self.chat)

        self.assertNotEqual(new_message.id, 300)
        self.assertNotEqual(new_message.created, created_at)
        self.assertNotEqual(new_message.sender_name, 'Toster')
