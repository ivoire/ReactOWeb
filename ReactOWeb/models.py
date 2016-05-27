from __future__ import unicode_literals

from django.db import models


class Message(models.Model):
    """
    This class is the exact clone of the one in ReactOBus.lib.db
    Assuming that this class is for Django while the other one is for
    SQLAlchemy.
    """
    topic = models.TextField(db_index=True)
    uuid = models.TextField(db_index=True)
    datetime = models.DateTimeField(db_index=True)
    username = models.TextField(db_index=True)
    data = models.TextField()

    class Meta:
        managed = False
        db_table = 'messages'

    def __str__(self):
        return "%s %s (%s)" % (self.topic, self.datetime, self.username)
