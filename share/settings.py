import os

DEBUG = os.environ.get("DEBUG", False)
ALLOWED_HOSTS = ["*"]
STATIC_ROOT = "/app/static"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

WHITENOISE_KEEP_ONLY_HASHED_FILES = True
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Load from environment
if "DB_ENGINE" in os.environ:
    DATABASES = {
        "default": {
            "ENGINE": os.environ["DB_ENGINE"],
            "NAME": os.environ["DB_NAME"],
            "USER": os.environ["DB_USER"],
            "PASSWORD": os.environ["DB_PASSWORD"],
            "HOST": os.environ["DB_HOST"],
            "PORT": os.environ["DB_PORT"],
        }
    }

# Add sentry if SENTRY_DSN is defined
if "SENTRY_DSN" in os.environ:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(dsn=os.environ["SENTRY_DSN"], integrations=[DjangoIntegration()])
