# import os 
# from . common import *


# SECRET_KEY = os.environ['SECRET_KEY']

# DEBUG = False 

# ALLOWED_HOSTS = ['*']



import os
from .common import *

SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')

DEBUG = False

ALLOWED_HOSTS = ['*']  # You can replace '*' with your Railway domain later


# SQLite database config
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Required for collectstatic
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Optional, if you have a static/ folder

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
