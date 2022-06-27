from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ceciestmasecretkeymouahahh"

DEBUG = True
INSTALLED_APPS += ("debug_toolbar",)  # and other apps for local development
ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "../litreview.sqlite3",
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_ROOT = "/chemin/d/acces/projet9/static/"
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "../static",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "../static/media/"
