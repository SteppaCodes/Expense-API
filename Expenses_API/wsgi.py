"""
WSGI config for Expenses_API project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from decouple import config

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'Expenses_API.settings.{config("SETTINGS")}')


application = get_wsgi_application()
app = application

