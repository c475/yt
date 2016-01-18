from django.http import HttpResponseRedirect


class NotLoggedInMixin(object):
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_anonymous():
            return super(NotLoggedInMixin, self).dispatch(*args, **kwargs)
        else:
            return HttpResponseRedirect('/')
