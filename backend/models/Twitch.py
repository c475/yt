from django.db import models


class Twitch(models.Model):
    title = models.CharField(max_length=128)
    url = models.CharField(max_length=128)
    streamer = models.CharField(max_length=128)
    user = models.ForeignKey('backend.User')
    start = models.DateTimeField()
    stop = models.DateTimeField(blank=True, null=True, default=None)
    room = models.ForeignKey('backend.Room')

    class Meta:
        app_label = 'backend'
        db_table = 'twitch'
