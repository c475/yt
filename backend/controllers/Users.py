from django.forms.models import model_to_dict
from social.apps.django_app.default.models import UserSocialAuth
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator

from backend.models import User, Room


class Users(object):

    def __init__(self, room=None, user=None):
        self.per_page = 20

        if room is not None:
            self.room = Room.objects.filter(name=room)
            if self.room.exists():
                self.room = self.room[0]
            else:
                self.room = None
        else:
            self.room = None

        if user is not None:
            if isinstance(user, int):
                self.user = User.objects.filter(pk=user)

                if self.user.exists():
                    self.user = self.user[0]
                else:
                    self.user = None

            else:
                self.user = user

        else:
            self.user = None

    @property
    def allUsers(self):
        return User.objects.filter(room=self.room)

    def serialize(self, model_instance):
        ret = {}
        for field in model_instance._meta.fields:
            field_value = getattr(model_instance, field.name)
            if isinstance(field, models.DateTimeField):
                if field_value is None:
                    ret[field.name] = None
                else:
                    ret[field.name] = field_value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                ret[field.name] = field_value

        return ret

    def getActiveUsers(self):
        users = User.objects.filter(current_room=self.room)
        if users.exists():
            return [{'username': u.username, 'id': u.pk} for u in users]
        else:
            return []

    def logout(self):
        if self.user is not None:
            self.user.current_room = None
            self.user.save()

    # dumb
    def getUser(self, uid):
        try:
            return model_to_dict(User.objects.get(id=uid))
        except:
            return None

    def changeUsername(self):
        self.user.username = data["username"]
        self.user.save()
        return user.username

    def getPages(self):
        return Paginator(self.allUsers, self.per_page).page_range

    def getUsers(self, page):
        p = Paginator(self.allUsers, self.per_page)
        return [self.serialize(v) for v in p.page(page).object_list]
