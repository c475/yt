import json
import hashlib
import hmac
import base64

from django.contrib.auth import logout
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import ListView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.shortcuts import render_to_response

from mediacenter.settings import SOCIAL_AUTH_GOOGLE_PLUS_KEY
from credentials import CROSSBAR_KEY

from backend.controllers.Users import Users
from backend.controllers.System import System

from backend.models import Room

from frontend.forms.UserCreationForm import UserCreationForm


def custom_login(request, **kwargs):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    else:
        return login(request, **kwargs)


class UserCreate(NotLoggedInMixin, CreateView):
    model = User
    template_name = 'register.html'
    success_url = '/'
    form_class = UserCreationForm

    def get_success_url(self):
        new_user = authenticate(
            username=self.request.POST.get("username", None),
            password=self.request.POST.get("password1", None)
        )

        if new_user is not None:
            login(self.request, new_user)

        return super(UserCreate, self).get_success_url()


def generate_secret(val):
    return base64.b64encode(hmac.new(
        bytes(CROSSBAR_KEY).encode('utf-8'),
        bytes(val).encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest())


class NotLoggedInMixin(object):
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_anonymous():
            return super(NotLoggedInMixin, self).dispatch(*args, **kwargs)
        else:
            return HttpResponseRedirect('/')


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class Login(NotLoggedInMixin, TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['google_plus'] = SOCIAL_AUTH_GOOGLE_PLUS_KEY
        return context


class RoomSelect(LoggedInMixin, ListView):
    model = Room
    template_name = 'rooms-listing.html'
    paginate_by = 20


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
    key = generate_secret(request.user.username)

    if room == 'default':
        return render_to_response('base.html', context={
            'room': 'default',
            'user': request.user,
            'key': key
        })
    else:
        if room is not None and Room.objects.filter(name=room).exists():
            return render_to_response('base.html', context={
                'room': room,
                'user': request.user,
                'key': key
            })
        else:
            return HttpResponseRedirect('/rooms/default/')


@login_required
def logout(request):
    if request.user.is_authenticated():
        Users(user=request.user).logout()
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


# To implement
class RoomDelete(object):
    pass


class RoomUpdate(object):
    pass
