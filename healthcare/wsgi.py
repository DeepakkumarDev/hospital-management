"""
WSGI config for healthcare project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information, see:
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

# Set the default Django settings module for the 'healthcare' project.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare.settings.prod')

application = get_wsgi_application()
application = WhiteNoise(application)
