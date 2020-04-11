from rest_framework import routers
from .views import ChatViewSet, MessageViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'chats', ChatViewSet, basename='chat')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = router.urls
