from django.forms.models import model_to_dict
from social.apps.django_app.default.models import UserSocialAuth
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator

from backend.models import User


class UserController(object):

    def __init__(self, room=None):
        self.per_page = 20

        self.room = Room.objects.filter(name=room)
        if self.room.exists():
            self.room = self.room[0]
        else:
            raise Exception('Room %s does not exist' % (room,))

    @property
    def allUsers(self):
        return User.objects.filter(room=room)

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
        return [{"username": u.user.username, "id": u.user.id} for u in UserSocialAuth.objects.filter(user__room=self.room)]

    def logout(self, uid):
        sessions = Session.objects.all()
        for session in sessions:
            if int(session.get_decoded().get("_auth_user_id")) == uid:
                user = User.objects.get(pk=uid)
                user.current_room = None
                user.save()
                session.delete()
                break

        UserSocialAuth.objects.filter(user=User.objects.get(pk=uid)).delete()

    def getUser(self, uid):
        try:
            return model_to_dict(User.objects.get(id=uid))
        except:
            return None

    def changeUsername(self, data):
        user = User.objects.get(pk=data["id"])
        user.username = data["username"]
        user.save()
        return user.username

    def getPages(self):
        return Paginator(self.allUsers, self.per_page).page_range

    def getUsers(self, page):
        p = Paginator(self.allUsers, self.per_page)
        return [self.serialize(v) for v in p.page(page).object_list]
