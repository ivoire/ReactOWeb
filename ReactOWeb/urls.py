from django.conf.urls import include, url

import ReactOWeb.views as v
from ReactOWeb.feeds import MessageFeed


urlpatterns = [
    url(r'^$', v.home, name='home'),
    url(r'^messages/$', v.messages, name='messages'),
    url(r'^messages/rss/$', MessageFeed(), name="messages.rss"),
    url(r'^messages/(?P<pk>\d+)/$', v.messages_details, name='messages.details'),
    url(r'^api/1.0/messages/$', v.api_messages, name='api.messages'),
    url(r'^api/1.0/messages/(?P<pk>\d+)/', v.api_messages_details, name='api.messages.details'),
]
