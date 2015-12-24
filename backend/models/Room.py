from datetime import datetime
from django.core.validators import RegexValidator
from django.db import models

alnum = RegexValidator(r'^[0-9a-zA-Z]+$', 'Only alphanumeric characters are allowed.')

class Room(models.Model):
    name = models.CharField(max_length=128, unique=True, validators=[alnum])
    creator = models.ForeignKey('backend.User')
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    description = models.CharField(max_length=500)

    class Meta:
        app_label = 'backend'
        db_table = 'room'
