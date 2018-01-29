from .base import *
import os

# Load the secret key from environment variable
SECRET_KEY = os.environ['SECRET_KEY']

# Disable debugging
DEBUG = False
TEMPLATE_DEBUG = False

# Load server IP from environment variable
SERVER_IP = os.environ['SERVER_IP']
ALLOWED_HOSTS = [SERVER_IP]

STATIC_ROOT = "/var/www/example.com/static/"

SECURE_HSTS_SECONDS = 3600
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_PRELOAD = True
