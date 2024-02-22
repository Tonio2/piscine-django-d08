# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message

connected_users = {}


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        self.user = self.scope["user"]
        self.username = self.user.username

        if self.room_name not in connected_users:
            connected_users[self.room_name] = []
        connected_users[self.room_name].append(self.user.username)

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        last_messages = await self.get_last_messages(self.room_name)

        for message in last_messages:
            await self.send(
                text_data=json.dumps(
                    {
                        "message": message["content"],
                        "username": message["username"],
                        "timestamp": message["timestamp"],
                    }
                )
            )

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "user_list", "message": connected_users[self.room_name]},
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": "has joined the chat",
                "username": self.username,
            },
        )

    async def user_list(self, event):
        await self.send(
            text_data=json.dumps({"type": "user_list", "message": event["message"]})
        )

    @database_sync_to_async
    def get_last_messages(self, room_name):
        msgs = Message.objects.filter(room_name=room_name).order_by("-timestamp")[:3][
            ::-1
        ]
        data = []
        for msg in msgs:
            data.append(
                {
                    "content": msg.content,
                    "username": msg.user.username,
                    "timestamp": msg.timestamp.strftime("%d/%m/%Y, %H:%M:%S"),
                }
            )
        return data

    @database_sync_to_async
    def get_username(self, user):
        return user.username

    async def disconnect(self, close_code):
        connected_users[self.room_name].remove(self.user.username)

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "user_list", "message": connected_users[self.room_name]},
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": "has left the chat",
                "username": self.user.username,
            },
        )
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await database_sync_to_async(self.save_message)(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.message", "message": message, "username": self.username},
        )

    def save_message(self, message):
        Message.objects.create(
            room_name=self.room_name, user=self.scope["user"], content=message
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({"message": message, "username": username})
        )
