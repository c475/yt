import hmac
import hashlib
import base64

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError
from autobahn.wamp import auth

from sys import path
import os

paths = [
    '/srv/',
    '/srv/mediacenter',
    '/srv/frontend',
    '/srv/backend',
]

for p in paths:
    if p not in path:
        path.append(p)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django import setup
setup()

from redis_sessions.session import SessionStore

from backend.models import User
from backend.controllers.Youtube import Youtube
from backend.controllers.Users import Users
from backend.controllers.Chats import Chats
from backend.controllers.System import System

from credentials import CROSSBAR_KEY, CROSSBAR_SALT

from redis import Redis

USER_SOCKETS = {}


def generate_secret(val):
    return base64.b64encode(hmac.new(
        bytes(CROSSBAR_KEY).encode('utf-8'),
        bytes(val).encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest())


class Authenticator(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        def authenticate(realm, authid, details):
            cookie = None
            headers = details['transport']['http_headers_received']

            if 'cookie' not in headers:
                who = details['transport']['peer'].split(':')[1]
                if who == '127.0.0.1':
                    return {'secret': generate_secret(CROSSBAR_SALT), 'role': 'backend'}
                else:
                    raise ApplicationError('Bad request')

            sessioncookies = map(lambda x: x.strip(), headers['cookie'].split(';'))

            for c in sessioncookies:
                if c.startswith('sessionid'):
                    cookie = c.split('=')[1]
                    break

            if cookie is not None:
                r = Redis()
                session = SessionStore(session_key=cookie).load()

                if session and '_auth_user_id' in session:
                    try:
                        user = User.objects.get(pk=authid)
                    except:
                        user = None

                    if user is not None and str(user.pk) == authid:
                        USER_SOCKETS[details['session']] = session['_auth_user_id']
                        return {'secret': generate_secret(user.username), 'role': 'frontend'}
                    else:
                        return ApplicationError('Invalid authid')
                else:
                    raise ApplicationError('Bad session')
            else:
                raise ApplicationError('No cookie')

        yield self.register(authenticate, 'mcauthenticator')


class Mediacenter(ApplicationSession):

    def onConnect(self):
        self.join('mediacenter', [u'wampcra'], 'someguy')

    def onChallenge(self, challenge):
        s = auth.compute_wcs(generate_secret(CROSSBAR_SALT), challenge.extra['challenge'].encode('utf8'))
        return s.decode('ascii')

    @inlineCallbacks
    def onJoin(self, details):

        def printendpoint(endpoint):
            print(USER_SOCKETS)
            print(('='*20) + endpoint + ('='*20))

        def initialize(data):
            printendpoint('initialize')
            room = data['room']

            active_users = Users(room).getActiveUsers()

            self.publish(room + '.users', 'list', active_users)

            return {
                'users': active_users,
                'chats': Chats(room).getChat(),
                'playing': Youtube(room).getCurrentlyPlaying(),
                'videos': Youtube(room).getPlaylist(),
                'historyPages': Youtube(room).getPages(),
                'userPages': Users(room).getPages(),
                'rooms': System().getRooms()
            }

        def sendChat(data):
            printendpoint('sendChat')
            print(data)
            room = data['room']
            self.publish(
                room + '.chat',
                Chats(room).sendChat(uid=data['uid'], content=data['content'])
            )

        def queueVideo(data):
            printendpoint('queueVideo')
            print(data)

            room = data['room']
            self.publish(
                room + '.playlist',
                Youtube(room).queueVideo(data['video']),
                Youtube(room).getPages()
            )

        def deQueueVideo(data):
            printendpoint('deQueueVideo')
            print(data)
            room = data['room']
            self.publish(
                room + '.playlist',
                Youtube(room).deQueueVideo(data['video'])
            )

        def playVideo(data):
            printendpoint('playVideo')
            print(data)
            room = data['room']

            self.publish(
                room + '.video',
                'play',
                Youtube(room).playVideo(data['video'])
            )

        def pauseVideo(data):
            printendpoint('pauseVideo')
            print(data)
            self.publish(data['room'] + '.video', 'pause')

        def resumeVideo(data):
            printendpoint('resumeVideo')
            print(data)
            self.publish(data['room'] + '.video', 'resume')

        def endVideo(data):
            printendpoint('endVideo')
            room = data['room']
            print(data)
            self.publish(
                room + '.video',
                'end',
                Youtube(room).endVideo(),
                Youtube(room).getPlaylist()
            )

        def getVideoHistory(data):
            printendpoint('getHistory')
            print(data)
            try:
                return Youtube(data['room']).getHistory(data['page'])
            except Exception, e:
                print(e)

        def createRoom(data):
            printendpoint('createRoom')
            print(data)
            rooms = System().getRooms()
            self.publish('rooms', rooms)

        def logout(data):
            printendpoint('logout')
            self.publish(data['room'] + '.users', 'list', Users().getActiveUsers())

        yield self.register(initialize, 'initialize')
        yield self.register(sendChat, 'sendChat')
        yield self.register(queueVideo, 'queueVideo')
        yield self.register(deQueueVideo, 'deQueueVideo')
        yield self.register(playVideo, 'playVideo')
        yield self.register(pauseVideo, 'pauseVideo')
        yield self.register(resumeVideo, 'resumeVideo')
        yield self.register(endVideo, 'endVideo')
        yield self.register(getVideoHistory, 'getVideoHistory')
        yield self.register(logout, 'logout')
        yield self.register(createRoom, 'createRoom')
