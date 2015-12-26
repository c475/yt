from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError


class Authenticator(ApplicationSession):

   def onConnect(self):
      print("CONNECT")
      raw_input()

   @inlineCallbacks
   def onJoin(self, details):

      def authenticate(realm, authid, details):
         print("authenticate called: realm = '{}', authid = '{}', details = '{}'".format(realm, authid, details))

         if authid:
            return {'secret': 'password', 'role': 'user', 'authid': '670'}
         else:
            raise ApplicationError('nope')

      yield self.register(authenticate, 'mcauthenticator')
