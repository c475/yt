import requests
import datetime
from backend.models import Twitch, Room

from django.forms.models import model_to_dict


class TwitchController(object):

    def __init__(self, room=None):
        self.endpoint = 'https://api.twitch.tv/kraken/'
        self.session = requests.Session()
        self.session.headers.update({
            'Client-ID': '8hgbbx82le28zpin9dqx1ybnolsrai1',
            'Accept': 'application/vnd.twitchtv.v3+json'
        })

        if room is not None:
            room = Room.objects.filter(name=room)
            if room.exists():
                self.room = room[0]
            else:
                raise Exception('Room does not exist: %s' % (room,))
        else:
            self.room = None

    @property
    def currentlyStreaming(self):
        return Twitch.objects.filter(room=self.room).exclude(start=None).filter(stop=None)

    def getTopGames(self):
        games = self.session.get(self.endpoint + 'games/top/?limit=100')
        return games.json()

    def channelsByGame(self, game):
        channels = self.session.get(
            self.endpoint + 'streams/',
            params={
                'game': game,
                'limit': 25,
                'stream_type': 'live'
            }
        )

        return channels.json()

    def startStream(self, user, stream):
        url = 'https://player.twitch.com/{}?embed=1'.format(stream['name'])

        stream = Twitch.objects.create(
            game=stream['game'],
            title=stream['status'],
            url=url,
            streamer=stream['name'],
            user_id=user,
            start=datetime.datetime.now(),
            room=self.room
        )

        stream = model_to_dict(stream)
        stream['start'] = stream['start'].strftime('%Y-%m-%d %H:%M:%S')
        stream['frame'] = '<iframe class="videoplayer" src="{}" frameborder="0" scrolling="no" allowfullscreen="" webkitallowfullscreen="" mozallowfullscreen=""></iframe>'.format(stream['url'])

        return stream

    def endStream(self):
        streaming = self.currentlyStreaming

        if streaming.exists():
            streaming = streaming[0]
            streaming.stop = datetime.datetime.now()
            streaming.save()
