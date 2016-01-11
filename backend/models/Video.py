from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=200)
    video_id = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    thumbnail = models.URLField()
    active = models.BooleanField(default=False, db_index=True)
    finished = models.BooleanField(default=False, db_index=True)
    user = models.ForeignKey("backend.User")

    start = models.DateTimeField(blank=True, null=True, default=None)
    stop = models.DateTimeField(blank=True, null=True, default=None)

    last_pause = models.DateTimeField(blank=True, null=True, default=None)
    last_position = models.FloatField(blank=True, null=True, default=None)

    # NULL: video is not active
    # 0: paused
    # 1: playing
    state = models.PositiveSmallIntegerField(blank=True, null=True, default=None)

    room = models.ForeignKey('backend.Room')

    class Meta:
        app_label = "backend"
        db_table = "video"
