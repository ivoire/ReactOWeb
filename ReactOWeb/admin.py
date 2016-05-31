from django.contrib import admin

from ReactOWeb.models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('topic', 'uuid', 'datetime', 'username')
    list_filter = ('topic', 'username')

admin.site.register(Message, MessageAdmin)
