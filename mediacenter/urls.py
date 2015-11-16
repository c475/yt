from django.conf.urls import patterns, include, url
from frontend.views import *


urlpatterns = patterns('',
    url(r'^rooms/$', RoomSelect.as_view()),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^login/$', Login.as_view()),
    url(r'^logout/$', logout),
    url(r'^index/$', Index.as_view()),
    url(r'^$', Index.as_view()),
)
