from .base import *

import warnings

# Enable debugging
DEBUG = True
TEMPLATE_DEBUG = True

# https://github.com/evansd/whitenoise/issues/215
warnings.filterwarnings("ignore", message="No directory at", module="whitenoise.base")

# https://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
staticfiles_app_index = INSTALLED_APPS.index("django.contrib.staticfiles")
INSTALLED_APPS.insert(staticfiles_app_index, "whitenoise.runserver_nostatic")
