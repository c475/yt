import datetime

from django.forms.models import model_to_dict
from django.db import models
from django.core.paginator import Paginator

from backend.models import Video, User, Room


class Youtube(object):

    def __init__(self, room):
        self.per_page = 20
        self.room = Room.objects.filter(name=room)
        if self.room.exists():
            self.room = self.room[0]
        else:
            raise Exception('Room %s does not exist' % (room,))

    @property
    def queuedVideos(self):
        return Video.objects.filter(
            active=False
        ).filter(
            finished=False
        ).filter(
            room=self.room
        )

    @property
    def currentlyPlaying(self):
        return Video.objects.filter(
            active=True
        ).filter(
            room=self.room
        )

    @property
    def allVideos(self):
        return Video.objects.filter(room=self.room)

    def getCurrentlyPlaying(self):
        playing = self.currentlyPlaying

        if playing.exists():

            playing = playing[0]
            ret = model_to_dict(playing)
            now = datetime.datetime.now()

            if playing.last_position:
                if playing.state == 1:
                    ret['start_seconds'] = (now - ret['last_pause'].replace(tzinfo=None)).seconds + playing.last_position
                else:
                    ret['start_seconds'] = playing.last_position
            else:
                ret['start_seconds'] = (now - ret['start'].replace(tzinfo=None)).seconds

            ret['start'] = ret['start'].strftime("%Y-%m-%d %H:%M:%S")
            del ret['last_pause']
            return ret

        else:
            return None

    def serialize(self, model_instance):
        ret = {}
        for field in model_instance._meta.fields:
            field_value = getattr(model_instance, field.name)
            if isinstance(field, models.DateTimeField):
                if field_value is None:
                    ret[field.name] = None
                else:
                    ret[field.name] = field_value.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(getattr(model_instance, field.name), (User, Room)):
                ret[field.name] = self.serialize(getattr(model_instance, field.name))
            else:
                ret[field.name] = field_value

        return ret

    def queueVideo(self, video):
        Video.objects.create(
            title=video["snippet"]["title"],
            video_id=video["id"]["videoId"],
            thumbnail=video["snippet"]["thumbnails"]["default"]["url"],
            description=video["snippet"]["description"],
            user_id=video["uid"],
            room=self.room
        )

        return self.getPlaylist()

    def deQueueVideo(self, video):
        video = Video.objects.get(pk=video["id"])
        video.finished = True
        video.save()
        return self.getPlaylist()

    def playVideo(self, video):
        video = Video.objects.get(pk=video["id"])
        video.active = True
        video.state = 1
        video.start = datetime.datetime.now()
        video.save()

        video = model_to_dict(video)
        video["start"] = video["start"].strftime("%Y-%m-%d %H:%M:%S")

        return video

    def endVideo(self):
        playing = self.currentlyPlaying

        if playing.exists():
            playing = playing[0]
            playing.finished = True
            playing.active = False
            playing.stop = datetime.datetime.now()
            playing.save()

        playlist = self.queuedVideos

        if playlist.exists():
            return self.playVideo({"id": playlist[0].id})
        else:
            return None

    def pauseVideo(self, position):
        playing = self.currentlyPlaying
        if playing.exists():
            playing = playing[0]
            playing.last_position = position
            playing.state = 0
            playing.save()

    def resumeVideo(self, position):
        playing = self.currentlyPlaying
        if playing.exists():
            playing = playing[0]
            playing.state = 1
            playing.last_pause = datetime.datetime.now()
            playing.last_position = position
            playing.save()

    def getPlaylist(self):
        queued_videos = self.queuedVideos

        if queued_videos.exists():
            videos = []
            for video in queued_videos:
                user = model_to_dict(video.user)
                user["last_login"] = user["last_login"].strftime("%Y-%m-%d %H:%M:%S")
                user["date_joined"] = user["date_joined"].strftime("%Y-%m-%d %H:%M:%S")

                video = model_to_dict(video)
                video["user"] = user
                videos.append(video)

            return videos

    def cleanUp(self, **kwargs):
        queued = self.queuedVideos
        playing = self.currentlyPlaying
        now = datetime.datetime.now()

        for video in queued:
            video.finished = True
            video.save()

        if playing.exists():
            playing = playing[0]
            playing.active = False
            playing.finished = True
            playing.stop = now
            playing.save()

    def getPages(self):
        return Paginator(self.allVideos, self.per_page).page_range

    def getHistory(self, page):
        p = Paginator(self.allVideos, self.per_page)
        return [self.serialize(v) for v in p.page(page).object_list]
