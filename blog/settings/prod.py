import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from django.core.management.utils import get_random_secret_key

from .base import *

SENTRY_DSN = os.environ.get("SENTRY_DSN")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )

# Load the secret key from environment variable
SECRET_KEY = os.environ.get("SECRET_KEY", get_random_secret_key())

HOSTNAME = os.environ.get("HOSTNAME", "localhost")

# Load server IP from environment variable
ALLOWED_HOSTS = [HOSTNAME]

CSRF_TRUSTED_ORIGINS = [f"https://{HOSTNAME}"]

SECURE_HSTS_SECONDS = 31_536_000
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_PRELOAD = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/data/db.sqlite3",
    }
}
