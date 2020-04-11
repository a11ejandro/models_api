from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from unittest.mock import patch, PropertyMock
import json
from gpt2.views import ChatViewSet
from gpt2.serializers import ChatDetailsSerializer, ChatPreviewSerializer
from .factories import ChatFactory, UserFactory


class ChatViewTestCase(APITestCase):
    def setUp(self):
        self.first_user = UserFactory.create()
        self.first_chat = ChatFactory(user=self.first_user)

        self.second_user = UserFactory.create()
        self.second_chat = ChatFactory(user=self.second_user)

    def testListLoginRequired(self):
        response = self.client.get(path='/gpt2/chats')
        self.assertEqual(response.status_code, 401)

        self._set_token()
        response = self.client.get(path='/gpt2/chats')
        self.assertEqual(response.status_code, 200)

    @patch('gpt2.views.ChatPreviewSerializer')
    def testList(self, mock_preview_serializer):
        mock_preview_serializer.return_value = ChatPreviewSerializer(self.first_chat)
        self._set_token()
        self.client.get(path='/gpt2/chats')
        args, kwargs = mock_preview_serializer.call_args

        self.assertTrue(len(args[0]), 2)

    def testRetrieveLoginRequired(self):
        response = self.client.get(path='/gpt2/chats/' + str(self.first_chat.pk))
        self.assertEqual(response.status_code, 401)
        self._set_token()
        response = self.client.get(path='/gpt2/chats/' + str(self.first_chat.pk))
        self.assertEqual(response.status_code, 200)

    @patch('gpt2.views.ChatDetailsSerializer')
    def testRetrieve(self, mock_details_serializer):
        mock_details_serializer.return_value = ChatDetailsSerializer(self.first_chat)

        self._set_token()
        response = self.client.get(path='/gpt2/chats/' + str(self.first_chat.pk))

        chat_json = json.loads(response.content)
        self.assertEqual(chat_json['name'], self.first_chat.name)
        # Check the correct serializer class was used
        mock_details_serializer.assert_called_once()


    def testCreateLoginRequired(self):
        response = self.client.post('/gpt2/chats', {'name': 'Antonio'})
        self.assertEqual(response.status_code, 401)


    @patch.object(ChatDetailsSerializer, 'is_valid', return_value=False)
    @patch.object(ChatDetailsSerializer, 'errors', new_callable=PropertyMock, return_value={})
    def testCreateInvalid(self, mock_is_valid, mock_errors):
        self._set_token()
        response = self.client.post('/gpt2/chats', {'name': 'Antonio'})
        result_json = json.loads(response.content)
        self.assertEqual(result_json['errors'], {})

    @patch.object(ChatDetailsSerializer, 'is_valid', return_value=True)
    @patch.object(ChatDetailsSerializer, 'data', new_callable=PropertyMock, return_value={})
    @patch.object(ChatDetailsSerializer, 'save', return_value={})
    def testCreateValid(self, mock_is_valid, mock_data, mock_save):
        self._set_token()
        response = self.client.post('/gpt2/chats', {'name': 'Antonio'})
        mock_save.assert_called_once()
        self.assertEqual(response.status_code, 200)


    ### PRIVATE ###
    def _set_token(self):
        token = Token.objects.get(user__id=self.first_user.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


