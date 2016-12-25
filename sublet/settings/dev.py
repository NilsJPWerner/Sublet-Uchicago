# Load defaults in order to then add/override with dev-only settings
from defaults import *
import os

DEBUG = True

SECRET_KEY = "8cb_+#9o)2&bzeefm#03iio2f$e1+k*skak0zje_i++ub=x@-1"

RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_PROXY = 'http://127.0.0.1:8000'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sublet',
        'USER': 'sublet',
        'PASSWORD': 'password',
        'HOST': '',
        'PORT': '',
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'nils.jp.werner@gmail.com'
EMAIL_HOST_PASSWORD = 'paqltnkxxaauugrd'