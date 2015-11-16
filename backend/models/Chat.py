from django.db import models


class Chat(models.Model):
    user = models.ForeignKey("backend.User")
    date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=500)
    room = models.ForeignKey('backend.Room')

    class Meta:
        app_label = "backend"
        db_table = "chat"
