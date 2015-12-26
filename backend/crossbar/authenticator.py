from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError

from sys import path
import os

paths = [
    '/srv/',
    '/srv/mediacenter',
    '/srv/frontend',
    '/srv/backend',
    '/srv/backend/crossbar'
]

for p in paths:
    if p not in path:
        path.append(p)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django import setup
setup()


class Authenticator(ApplicationSession):

   @inlineCallbacks
   def onJoin(self, details):

      def authenticate(realm, authid, details):
         print(realm, authid, details)

         if authid:
            return {'secret': 'password', 'role': 'user', 'authid': '670'}
         else:
            raise ApplicationError('nope')

      yield self.register(authenticate, 'mcauthenticator')
