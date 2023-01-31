from django.urls import re_path
from djangochannelsrestframework.consumers import view_as_consumer


from . import consumers

websocket_urlpatterns = [
    re_path(r'chat/ws/', consumers.ChatConsumer.as_asgi()),
    re_path(r"^chat/ws/api/$", view_as_consumer(consumers.ChatAPIConsumer)),
]