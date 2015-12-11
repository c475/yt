from datetime import datetime
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=128, unique=True)
    creator = models.ForeignKey('backend.User')
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    description = models.CharField(max_length=500)

    class Meta:
        app_label = 'backend'
        db_table = 'room'
