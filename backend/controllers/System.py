import datetime
from backend.models import Room, User


class System(object):

    def __init__(self, room=None, user=None):
        if room is not None:
            room = Room.objects.filter(name=room)
            if room.exists():
                self.room = room[0]
            else:
                self.room = None

        else:
            self.room = None

        if user is not None:
            user = User.objects.filter(pk=int(user))
            if user.exists():
                self.user = user[0]
            else:
                self.user = None

        else:
            self.user = None

    def getRooms(self):
        return [{'id': r.id, 'name': r.name} for r in Room.objects.all()]

    def createRoom(self, name):
        if self.user is None:
            return None

        if Room.objects.filter(name=name).exists():
            return None
        else:
            new_room = Room.objects.create(
                name=name,
                creator=self.user,
                date_created=datetime.datetime.now()
            )

        return getRooms()

    def joinRoom(self, room):
        if self.user is None:
            return None

        room = Room.objects.filter(name=room)

        if room.exists():
            self.user.current_room = room[0]
            self.user.save()

        else:
            self.user.current_room = Room.objects.all()[0]
