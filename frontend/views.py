from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from mediacenter.settings import SOCIAL_AUTH_GOOGLE_PLUS_KEY, GOOGLE_ANALYTICS

from backend.controllers.UserController import UserController
from backend.models import Room


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
        context['google_analytics'] = GOOGLE_ANALYTICS
        return context


class RoomSelect(LoggedInMixin, TemplateView):
    template_name = 'rooms.html'

    def get_context_data(self, **kwargs):
        context = super(RoomSelect, self).get_context_data(**kwargs)
        context['rooms'] = Room.objects.all()
        context['google_analytics'] = GOOGLE_ANALYTICS
        return context


class Index(LoggedInMixin, TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['google_analytics'] = GOOGLE_ANALYTICS

        room = self.request.GET.get('room')

        if room is not None and Room.objects.filter(name=room).exists():
            context['room'] = room
        else:
            context['room'] = 'default'

        return context


@login_required
def logout(request):
    if request.user.is_authenticated():
        UserController(user=request.user).logout()
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
