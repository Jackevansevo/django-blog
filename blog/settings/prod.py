from .base import *
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

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Load server IP from environment variable
ALLOWED_HOSTS = [SERVER_IP, DOMAIN_NAME]

# Disable debugging
DEBUG = False
TEMPLATE_DEBUG = False

# Add GZIP middleware class
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SECURE_HSTS_SECONDS = 3600
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_PRELOAD = True
