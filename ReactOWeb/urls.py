from django.conf.urls import include, url

import ReactOWeb.views

urlpatterns = [
    url(r'^api/1.0/messages', ReactOWeb.views.api_messages, name='api.messages'),
]
