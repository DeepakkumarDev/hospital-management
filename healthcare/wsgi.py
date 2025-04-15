"""
WSGI config for healthcare project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""
import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare.settings.dev')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare.settings.prod')

application = get_wsgi_application()
application = WhiteNoise(application)