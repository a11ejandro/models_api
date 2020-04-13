import factory
from factory import faker

from django.contrib.auth.models import User
from gpt2.models import Chat, Message

FAKER = faker.faker.Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = FAKER.email()
    first_name = FAKER.first_name()
    last_name = FAKER.last_name()
    username = factory.Sequence(lambda n: "User %03d" % n)


class ChatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Chat

    name = 'The girl has no name'
    user = factory.SubFactory(UserFactory)


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    body = 'My body is a cage'
    sender_name = 'Mr Alex'
    chat = factory.SubFactory(ChatFactory)
