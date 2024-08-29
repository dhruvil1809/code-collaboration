import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import File

class CodeEditorConsumer(WebsocketConsumer):
    def connect(self):
        self.file_id = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = f'code_{self.file_id}'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')
        message = text_data_json.get('message')

        if action == 'broadcast':
            # Broadcast message to all connected clients without saving
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'code_message',
                    'message': message
                }
            )

        elif action == 'save':
            # Save the file content in the database and broadcast the final content
            file = File.objects.get(pk=self.file_id)
            file.content = message
            file.save()

            # Notify all clients that the file has been saved
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'code_message',
                    'message': message
                }
            )

    def code_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
