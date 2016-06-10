from django.contrib.syndication.views import Feed

from ReactOWeb.models import Message


class MessageFeed(Feed):
    title = "Message feed"
    link = "/messages/"
    description = "Feed of messages on the bus"

    def items(self):
        return Message.objects.all().order_by('-datetime')[:20]

    def item_title(self, item):
        return "%d - %s" % (item.pk, item.topic)

    def item_description(self, item):
        return "%s - %s: %s" % (item.datetime, item.uuid, item.pp_data())


