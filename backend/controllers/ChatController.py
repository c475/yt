from backend.models import Room, Chat


class ChatController(object):

    def __init__(self, room):
        self.room = Room.objects.filter(name=room)
        if self.room.exists():
            self.room = self.room[0]
        else:
            raise Exception('Room %s does not exist' % (room,))

    def getChat(self, **kwargs):
        chats = []
        last_50 = reversed(Chat.objects.filter(room=self.room).order_by("-id")[:20])

        for chat in last_50:
            chats.append({
                "content": chat.content,
                "date": chat.date.strftime("%Y-%m-%d %H:%M:%S"),
                "user": {
                    "username": chat.user.username,
                    "id": chat.user.id
                }
            })

        return chats

    def sendChat(self, **kwargs):
        chat = Chat.objects.create(
            user_id=kwargs["uid"],
            content=kwargs["content"],
            room=self.room
        )

        return {
            "user": {
                "username": chat.user.username,
                "id": chat.user.id
            },
            "date": chat.date.strftime("%Y-%m-%d %H:%M:%S"),
            "content": kwargs["content"]
        }
