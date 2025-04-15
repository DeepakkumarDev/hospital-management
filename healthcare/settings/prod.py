import os
from .common import *

# Secret key: fallback for local or dev environments
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')

# Disable debug for production
DEBUG = False

# Allow all hosts (replace '*' with specific domain in real production)
ALLOWED_HOSTS = ['*']

# SQLite database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# settings.py

CSRF_COOKIE_SECURE = True  # Ensure CSRF cookies are only sent over HTTPS (for production)
CSRF_COOKIE_HTTPONLY = True  # Ensure CSRF cookies are not accessible via JavaScript
CSRF_TRUSTED_ORIGINS = [
    'https://hospital-management-production-25a0.up.railway.app',
]  # Add your production domain here



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # collectstatic will copy here
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Your project's static folder

# WhiteNoise settings (for serving static files in production)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
