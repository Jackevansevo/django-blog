from .base import *
import raven
import os

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    """Get the environment variable or return exception"""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Set the {var_name} environment variable"
        raise ImproperlyConfigured(error_msg)


# Load the secret key from environment variable
SECRET_KEY = get_env_variable('SECRET_KEY')
SERVER_IP = get_env_variable('SERVER_IP')
DOMAIN_NAME = get_env_variable('DOMAIN_NAME')

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat',
]


RAVEN_CONFIG = {
    'dsn': get_env_variable('SENTRY_URL'),
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}


STATIC_ROOT = os.path.join(BASE_DIR, 'assets/')

# Load server IP from environment variable
ALLOWED_HOSTS = [SERVER_IP, DOMAIN_NAME]

# Disable debugging
DEBUG = False
TEMPLATE_DEBUG = False

SECURE_HSTS_SECONDS = 31536000
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_PRELOAD = True
