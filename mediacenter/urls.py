from django.conf.urls import patterns, include, url
from frontend.views import *


urlpatterns = patterns('',
    url(r'^rooms/$', RoomSelect.as_view()),
    url(r'^rooms/(?P<room>\w+)/$', index),
    url(r'^create/$', RoomCreate.as_view()),

    url(r"^login/$", custom_login, name="login"),
    url(r'^logout/$', logout),
    url(r"^register/$", UserCreate.as_view()),

    url(r'^$', RoomSelect.as_view()),
)
