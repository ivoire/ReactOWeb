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

from django.conf.urls import include, url

import ReactOWeb.views as v
from ReactOWeb.feeds import MessageFeed


urlpatterns = [
    url(r"^$", v.home, name="home"),
    url(r"^charts/", v.charts, name="charts"),
    url(r"^messages/$", v.messages, name="messages"),
    url(r"^messages/rss/$", MessageFeed(), name="messages.rss"),
    url(r"^messages/(?P<pk>\d+)/$", v.messages_details, name="messages.details"),
    url(r"^messages/live/$", v.messages_live, name="messages.live"),
    url(r"^api/1.0/messages/$", v.api_messages, name="api.messages"),
    url(
        r"^api/1.0/messages/(?P<pk>\d+)/",
        v.api_messages_details,
        name="api.messages.details",
    ),
]
