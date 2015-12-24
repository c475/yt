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
]

for p in paths:
    if p not in path:
        path.append(p)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django import setup
setup()


from backend.controllers.Youtube import Youtube
from backend.controllers.Users import Users
from backend.controllers.Chats import Chats
from backend.controllers.System import System


class Mediacenter(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        def authenticate(realm, authid, details):
            print(realm, authid, details)
            return {'secret': 'testsecret', 'role': 'user'}

        def printendpoint(endpoint):
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

        yield self.register(authenticate, 'mcauthenticator')
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
