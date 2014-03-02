from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9hd312fage<>!*Jjav12&!yhp0^pcvr2mwwruu_u=cxyu=1c0nos%*'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'tecnocial',
#         'USER': 'tecnocial',
#         'PASSWORD': 'tecnocial',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}