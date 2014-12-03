"""
Django settings for sakila project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# CLEARDB_DATABASE_URL: mysql://b6a1524783e940:3e36b7b3@us-cdbr-iron-east-01.cleardb.net/heroku_31d3d4d44109464?reconnect=true


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*4wlb4-(+b7!g1c)#99yhqu(xy-dm)1#wjuc2@q!rg_elxha04'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sakila_ok',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sakila.urls'

# WSGI_APPLICATION = 'sakila.wsgi.application'

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql', 
    #     'NAME': 'sakila_database',
    #     'USER': 'root',
    #     'PASSWORD': 'sakila_password',
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'sakila',
        'USER': 'kfares',
        'PASSWORD': 'kfares',
        'HOST':'mysql4.qatar.cmu.local',
        'PORT':'3334',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# Parse database configuration from $DATABASE_URL
# # import dj_database_url
# # DATABASES['default'] =  dj_database_url.config()

# # Honor the 'X-Forwarded-Proto' header for request.is_secure()
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# # Allow all host headers
# ALLOWED_HOSTS = ['*']

# # Static asset configuration
# import os
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# STATIC_ROOT = 'staticfiles'
# STATIC_URL = '/static/'

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, '../sakila_ok/static/'),
# )

# import sys
# import urlparse
# urlparse.uses_netloc.append('mysql')

# try:
#     # Check to make sure DATABASES is set in settings.py file.
#     # If not default to {}
#     if 'DATABASES' not in locals():
#         DATABASES = {}

#     if 'DATABASE_URL' in os.environ:
#         url = urlparse.urlparse(os.environ['DATABASE_URL'])

#         # Ensure default database exists.
#         DATABASES['default'] = DATABASES.get('default', {})

#         # Update with environment configuration.
#         DATABASES['default'].update({
#             'NAME': url.path[1:],
#             'USER': url.username,
#             'PASSWORD': url.password,
#             'HOST': url.hostname,
#             'PORT': url.port,
#         })


#         if url.scheme == 'mysql':
#             DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
# except Exception:
#     print 'Unexpected error:', sys.exc_info()