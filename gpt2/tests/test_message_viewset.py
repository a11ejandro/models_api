from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from unittest.mock import patch, PropertyMock
import json
from gpt2.views import MessageViewSet
from gpt2.serializers import MessageSerializer, ChatDetailsSerializer
from .factories import ChatFactory, UserFactory, MessageFactory


class MessageViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.chat = ChatFactory(user=self.user)


    def testCreateLoginRequired(self):
        response = self.client.post('/gpt2/messages', {'body': 'You are a parrot!'})
        self.assertEqual(response.status_code, 401)

    def testCreateWrongOwner(self):
        self._set_token()
        other_chat = ChatFactory()
        response = self.client.post('/gpt2/messages',
            {'body': 'You are a parrot!', 'chat': other_chat.pk})
        self.assertEqual(response.status_code, 403)


    @patch.object(MessageSerializer, 'is_valid', return_value=False)
    @patch.object(MessageSerializer, 'errors', 
        new_callable=PropertyMock, return_value={})
    def testCreateInvalid(self, mock_is_valid, mock_errors):
        self._set_token()
        response = self.client.post('/gpt2/messages',
            {'body': 'You are a parrot!', 'chat': self.chat.pk})
        result_json = json.loads(response.content)
        self.assertEqual(result_json['errors'], {})


    def testCreateChatNotFound(self):
        self._set_token()
        response = self.client.post('/gpt2/messages',
            {'body': 'You are a parrot!', 'chat': 3000})
        self.assertEqual(response.status_code, 404)


    @patch('gpt2.views.post_and_reply')
    @patch('gpt2.views.ChatDetailsSerializer')
    def testCreateValid(self, mock_chat_serializer, mock_post_and_reply):
        mock_post_and_reply.return_value = (True, None)
        mock_chat_serializer.return_value = ChatDetailsSerializer(self.chat)

        self._set_token()
        response = self.client.post('/gpt2/messages',
            {'body': 'You are a parrot', 'chat': self.chat.pk})
        mock_post_and_reply.assert_called_once()
        mock_chat_serializer.assert_called_once()
        self.assertEqual(response.status_code, 200)


    ### PRIVATE ###
    def _set_token(self):
        token = Token.objects.get(user__id=self.user.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

