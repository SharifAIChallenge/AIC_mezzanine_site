SECRET_KEY = "TOP_SECRET"

ALLOWED_HOSTS = ["aichallenge.sharif.edu", "aichallenge.sharif.edu:2016"]

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "DB_NAME",
        "USER": "DB_USERNAME",
        "PASSWORD": "DB_TOPSECRET_PASSWORD",
        "HOST": "localhost",
        "PORT": "5432",
    }
}


CACHE_MIDDLEWARE_SECONDS = 60

CACHE_MIDDLEWARE_KEY_PREFIX = "AIC_SITE"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "127.0.0.1:11211",
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"


EMAIL_HOST = 'smtp.somehost.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'some_user'
EMAIL_HOST_PASSWORD = 'TOPSECRET'
DEFAULT_FROM_EMAIL = 'YOUR NAME <someone@somehost>'


SFTP_STORAGE_HOST = 'localhost'
SFTP_STORAGE_ROOT = '/home/user/media'
SFTP_STORAGE_PARAMS = {'username': 'user'}


### STORAGE SETTINGS ###

from AIC_site.storage import SyncingStorage

BASE_AND_GAME_STORAGE = SyncingStorage(
    # 'storages.compat.FileSystemStorage',
    'storages.backends.hashpath.HashPathStorage',
    "storages.backends.sftpstorage.SFTPStorage")



