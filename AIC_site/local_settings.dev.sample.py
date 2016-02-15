# This file is exec'd from settings.py, so it has access to and can
# modify all the variables in settings.py.

# If this file is changed in development, the development server will
# have to be manually restarted because changes will not be noticed
# immediately.

DEBUG = True

SITE_ID = 1

# Make these unique, and don't share it with anybody.
SECRET_KEY = "A_TOP_SECRET_KEY"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "dev.db",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}


EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = 'webmaster@localhost'
EMAIL_HOST_PASSWORD = 'TOPSECRET'
EMAIL_PORT = 25
EMAIL_USE_TLS = True
"A_TOP_SECRET_KEY"


SFTP_STORAGE_HOST = 'localhost'
SFTP_STORAGE_ROOT = '/home/user/media'
SFTP_STORAGE_PARAMS = {'username': 'user'}

CELERY_ROUTES = {'queued_storage.tasks.Transfer': {'queue': 'filestorage_queue_main'},
                 'queued_storage.tasks.TransferAndDelete': {'queue': 'filestorage_queue_main'},
                 }


### STORAGE SETTINGS ###

from django.core.files.storage import FileSystemStorage

BASE_AND_GAME_STORAGE = FileSystemStorage()


