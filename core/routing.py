from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<user1>[^/]+)/(?P<user2>[^/]+)/(?P<product>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
]