from .base import *

# Enable debugging
DEBUG = True
TEMPLATE_DEBUG = True

INSTALLED_APPS.append("debug_toolbar")

INTERNAL_IPS = ["127.0.0.1"]

MIDDLEWARE.append(
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)
