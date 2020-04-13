from django.test import TestCase
from unittest.mock import patch, Mock
from gpt2.requests import Gpt2, Gpt2Chat
from .factories import ChatFactory, MessageFactory


class TestRequests(TestCase):
    @patch('gpt2.requests.urllib.request.urlopen')
    def testGpt2Request(self, urllib_mock):
        returned_obj = Mock()
        returned_obj.read = Mock(return_value='hi')
        urllib_mock.return_value = returned_obj

        result = Gpt2.request(a=1, b=2)
        _, kwargs = urllib_mock.call_args
        expected_kwargs = {'a': 1, 'b': 2}
        self.assertDictEqual(kwargs, {'data': expected_kwargs})
        self.assertEqual(result, 'hi')


class TestChat(TestCase):
    def setUp(self):
        self.chat = ChatFactory()
        self.gpt2_chat = Gpt2Chat(self.chat)

    # Override constant to smaller value to speed up test
    @patch('gpt2.requests.Gpt2Chat.LAST_MESSAGES_COUNT', 4)
    def testGpt2ChatUncompleteDialog(self):
        MessageFactory.create_batch(6, chat=self.chat)
        concatenated = self.gpt2_chat.uncomplete_dialog()
        # Take into account placeholder for empty reply
        self.assertEqual(len(concatenated.split('\n')), 5)

    @patch('gpt2.requests.Gpt2Chat.uncomplete_dialog')
    @patch('gpt2.requests.Gpt2.request')
    def testNextMessage(self, request_mock, dialog_mock):
        dialog_mock.return_value = 'hi'
        request_mock.return_value = 'bye'

        response = self.gpt2_chat.next_message()
        self.assertEqual(response, 'bye')
        _, kwargs = request_mock.call_args
        expected_kwargs = {
            'text': 'hi',
            'unconditional': False,
            'length': Gpt2Chat.LIMIT_MESSAGE_LENGTH,
        }
        self.assertDictEqual(kwargs, expected_kwargs)
