from django.forms.models import model_to_dict
from social.apps.django_app.default.models import UserSocialAuth
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator

from backend.models import User, Room


class UserController(object):

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
            self.user = User.objects.filter(pk=user)
            if self.user.exists():
                self.user = self.user[0]
            else:
                self.user = None

        else:
            self.user = None

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

    def logout(self):
        sessions = Session.objects.all()
        for session in sessions:
            if int(session.get_decoded().get("_auth_user_id")) == self.user.pk:
                self.user.current_room = None
                self.user.save()
                session.delete()
                break

        UserSocialAuth.objects.filter(user=self.user).delete()

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
