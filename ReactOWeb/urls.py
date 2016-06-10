from django.conf.urls import include, url

import ReactOWeb.views as v

urlpatterns = [
    url(r'^$', v.home, name='home'),
    url(r'^api/1.0/messages/$', v.api_messages, name='api.messages'),
    url(r'^api/1.0/messages/(?P<pk>\d+)/', v.api_messages_details, name='api.messages.details'),
]
