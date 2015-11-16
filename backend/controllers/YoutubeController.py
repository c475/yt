import datetime

from django.forms.models import model_to_dict
from django.db import models
from django.core.paginator import Paginator

from backend.models import Video, User, Room


class YoutubeController(object):

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
            playing=False
        ).filter(
            finished=False
        ).filter(
            room=self.room
        )

    @property
    def currentlyPlaying(self):
        return Video.objects.filter(
            playing=True
        ).filter(
            room=self.room
        )

    @property
    def allVideos(self):
        return Video.objects.filter(room=self.room)
    
    def getCurrentlyPlaying(self):
        playing = self.currentlyPlaying

        if playing.exists():
            now = datetime.datetime.now()

            playing = model_to_dict(playing[0])
            playing["start_seconds"] = (now - playing["start"].replace(tzinfo=None)).seconds
            playing["start"] = playing["start"].strftime("%Y-%m-%d %H:%M:%S")
            return playing
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
        video.playing = True
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
            playing.playing = False
            playing.stop = datetime.datetime.now()
            playing.save()

        playlist = self.queuedVideos

        if playlist.exists():
            return self.playVideo({"id": playlist[0].id})
        else:
            return None

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
            playing.playing = False
            playing.finished = True
            playing.stop = now
            playing.save()

    def getPages(self):
        return Paginator(self.allVideos, self.per_page).page_range

    def getHistory(self, page):
        p = Paginator(self.allVideos, self.per_page)
        return [self.serialize(v) for v in p.page(page).object_list]
