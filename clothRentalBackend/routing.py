from django.urls import re_path
from notifications import consumer
websocket_urlpatterns = [
    re_path(r'ws/notification/(?P<user_id>\w+)/$', consumer.NotificationConsumer.as_asgi()),
]