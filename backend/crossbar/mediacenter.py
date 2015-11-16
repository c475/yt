###############################################################################
#
# Copyright (C) 2014, Tavendo GmbH and/or collaborators. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
###############################################################################

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


from backend.controllers.YoutubeController import YoutubeController
from backend.controllers.UserController import UserController
from backend.controllers.ChatController import ChatController
from backend.controllers.System import System


class Mediacenter(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        def printendpoint(endpoint):
            print(('='*20) + endpoint + ('='*20))

        def initialize(data):
            printendpoint('initialize')
            room = data['room']

            active_users = UserController(room).getActiveUsers()

            self.publish(room + '.users', 'list', active_users)

            return {
                'users': active_users,
                'chats': ChatController(room).getChat(),
                'playing': YoutubeController(room).getCurrentlyPlaying(),
                'videos': YoutubeController(room).getPlaylist(),
                'historyPages': YoutubeController(room).getPages(),
                'userPages': UserController(room).getPages(),
                'rooms': System().getRooms()
            }

        def sendChat(data):
            printendpoint('sendChat')
            print(data)
            room = data['room']
            self.publish(
                room + '.chat',
                ChatController(room).sendChat(uid=data['uid'], content=data['content'])
            )

        def queueVideo(data):
            printendpoint('queueVideo')
            print(data)

            room = data['room']
            self.publish(
                room + '.playlist',
                YoutubeController(room).queueVideo(data['video']),
                YoutubeController(room).getPages()
            )

        def deQueueVideo(data):
            printendpoint('deQueueVideo')
            print(data)
            room = data['room']
            self.publish(
                room + '.playlist',
                YoutubeController(room).deQueueVideo(data['video'])
            )

        def playVideo(data):
            printendpoint('playVideo')
            print(data)
            room = data['room']

            self.publish(
                room + '.video',
                'play',
                YoutubeController(room).playVideo(data['video'])
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
                YoutubeController(room).endVideo(),
                YoutubeController(room).getPlaylist()
            )

        def getVideoHistory(data):
            printendpoint('getHistory')
            print(data)
            try:
                return YoutubeController(data['room']).getHistory(data['page'])
            except Exception, e:
                print(e)

        def createRoom(data):
            printendpoint('createRoom')
            print(data)
            rooms = System().getRooms()
            self.publish('rooms', rooms)

        # def getUsers(page):
        #     printendpoint("getUsers")
        #     return self.User.getUsers(page)

        def logout(data):
            printendpoint('logout')
            self.publish(data['room'] + '.users', 'list', UserController().getActiveUsers())

        # def changeUsername(data):
        #     return User.changeUsername(data)


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
        # yield self.register(changeUsername, 'changeUsername')
        yield self.register(createRoom, 'createRoom')
