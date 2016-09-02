# -*- coding: utf-8 -*-
# vim: set ts=4

# Copyright 2016 Rémi Duraffort
# This file is part of ReactOWeb.
#
# ReactOWeb is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ReactOWeb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with ReactOWeb.  If not, see <http://www.gnu.org/licenses/>

import json

from django.core.urlresolvers import reverse
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

    def get_absolute_url(self):
        return reverse('messages.details', args=[str(self.id)])

    def as_dict(self):
        return {"id": self.id,
                "topic": self.topic,
                "uuid": self.uuid,
                "datetime": self.datetime.isoformat(),
                "username": self.username,
                "data": json.loads(self.data)}

    def pp_data(self):
        return json.dumps(json.loads(self.data), sort_keys=True, indent=4)
