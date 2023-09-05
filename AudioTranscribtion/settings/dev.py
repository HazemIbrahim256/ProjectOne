from .common import *


DEBUG = True

SECRET_KEY = 'django-insecure-kmjv4h&_ffi(lc+@3qejx3@ig9pxq^i+wn2@!m-%q=jt6*!*^9'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}