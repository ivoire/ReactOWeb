FROM debian:buster-slim

LABEL maintainer="Rémi Duraffort <remi.duraffort@linaro.org>"

ENV DEBIAN_FRONTEND noninteractive

# Install dependencies
RUN apt-get update -q ;\
    apt-get install --no-install-recommends --yes gunicorn3 libjs-jquery python3 python3-pip python3-django python3-dateutil python3-psycopg2 python3-yaml ;\
    python3 -m pip install --upgrade whitenoise ;\
    # Cleanup
    apt-get clean ;\
    rm -rf /var/lib/apt/lists/*

# Add ReactOWeb sources
WORKDIR /app/
COPY ReactOWeb/ /app/ReactOWeb/
COPY share/settings.py /app/ReactOWeb/custom_settings.py
COPY share/urls.py /app/reactoweb/urls.py.orig

# Create and setup the Django project
RUN chmod 775 /app ;\
    django-admin startproject reactoweb /app ;\
    mv /app/reactoweb/urls.py.orig /app/reactoweb/urls.py ;\
    # Setup lavafed application
    echo "INSTALLED_APPS.append(\"ReactOWeb\")" >> /app/reactoweb/settings.py ;\
    echo "from ReactOWeb.custom_settings import *" >> /app/reactoweb/settings.py ;\
    # Migrate and collect static files
    python3 manage.py migrate --noinput ;\
    python3 manage.py collectstatic --noinput

COPY share/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
