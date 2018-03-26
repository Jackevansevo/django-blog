from .base import *

# Disable debugging
DEBUG = False
TEMPLATE_DEBUG = False

# Use a faster password hasher during testing
PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)

# Disable unnecessary middleware classes
INSTALLED_APPS = [
    'posts.apps.PostsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
]

# Disable unnecessary middleware classes
MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# Use a dummy cache
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}
