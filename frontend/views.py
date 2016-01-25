import json
import hashlib
import hmac
import base64

from django.contrib.auth import authenticate
from django.contrib.auth import login as login_auth

from django.contrib.auth.views import login as login_view
from django.http import HttpResponseRedirect

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import ListView

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from credentials import CROSSBAR_KEY

from backend.models import Room
from backend.models import User

from frontend.forms.UserCreationForm import UserCreationForm
from frontend.mixins.LoggedInMixin import LoggedInMixin
from frontend.mixins.NotLoggedInMixin import NotLoggedInMixin


def custom_login(request, **kwargs):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    else:
        return login_view(request, **kwargs)


class UserCreate(NotLoggedInMixin, CreateView):
    model = User
    template_name = 'registration/register.html'
    success_url = '/'
    form_class = UserCreationForm

    def get_success_url(self):
        new_user = authenticate(
            username=self.request.POST.get("username", None),
            password=self.request.POST.get("password1", None)
        )

        if new_user is not None:
            login_auth(self.request, new_user)

        return super(UserCreate, self).get_success_url()


def generate_secret(val):
    return base64.b64encode(hmac.new(
        bytes(CROSSBAR_KEY).encode('utf-8'),
        bytes(val).encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest())


class Login(NotLoggedInMixin, TemplateView):
    template_name = 'login.html'


class RoomSelect(LoggedInMixin, ListView):
    model = Room
    template_name = 'rooms-listing.html'
    paginate_by = 20

    def get_queryset(self):
        return sorted(
            super(RoomSelect, self).get_queryset(),
            key=lambda x: x.user_total
        )


class RoomCreate(LoggedInMixin, CreateView):
    model = Room
    template_name = 'rooms-create.html'
    fields = ['name', 'description']

    def form_valid(self, form):
        new_room = Room.objects.create(
            name=form.instance.name,
            description=form.instance.description,
            creator=self.request.user
        )

        return HttpResponseRedirect('/rooms/' + form.instance.name + '/')


@login_required
def index(request, room=None):
    if room == 'default':
        request.user.current_room_id = 1
        request.user.save()
        return render_to_response('base.html', context={
            'room': 'default',
            'user': request.user,
            'key': generate_secret(request.user.username)
        })
    else:
        room = Room.objects.filter(name=room)
        if room.exists():
            room = room[0]
            request.user.current_room_id = room.pk
            request.user.save()
            return render_to_response('base.html', context={
                'room': room.name,
                'user': request.user,
                'key': generate_secret(request.user.username)
            })
        else:
            return HttpResponseRedirect('/rooms/default/')


# To implement
class RoomDelete(object):
    pass


class RoomUpdate(object):
    pass
