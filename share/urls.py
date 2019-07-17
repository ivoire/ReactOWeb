from django.conf.urls import include, url
from django.contrib import admin
from ReactOWeb import urls as row_urls

urlpatterns = [url(r"^admin/", admin.site.urls), url(r"^", include(row_urls))]
