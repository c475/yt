from datetime import datetime
from django.core.validators import RegexValidator
from django.db import models
from backend.models import User

alnum = RegexValidator(r'^[0-9a-zA-Z_\-]+$', 'Only alphanumeric characters are allowed.')


class Room(models.Model):
    name = models.CharField(max_length=128, unique=True, validators=[alnum])
    creator = models.ForeignKey('backend.User')
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    description = models.CharField(max_length=500)

    @property
    def user_total(self):
        return User.objects.filter(current_room_id=self.id).count()

    class Meta:
        app_label = 'backend'
        db_table = 'room'
