import dj_database_url
from defaults import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()
DATABASES['default']['CONN_MAX_AGE'] = 500

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Should get an email servers