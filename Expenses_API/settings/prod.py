from .base import *


DEBUG = False


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("PROD_PG_DB"),
        "URL": config("POSTGRES_URL"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("PROD_PG_PASSWORD"),
        "HOST": config("PROD_PG_HOST"),
        "PORT": config("PROD_PG_PORT"),
    }
}


