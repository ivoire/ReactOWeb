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

from django.contrib import admin

from ReactOWeb.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ("topic", "uuid", "datetime", "username")
    list_filter = ("topic", "username")


admin.site.register(Message, MessageAdmin)
