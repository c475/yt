from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError


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
