from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/code/<int:pk>/', consumers.CodeEditorConsumer.as_asgi()),
]
