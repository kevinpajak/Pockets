"""
Django settings for protoplate project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#_=l+(vbc!@735a@*^@0!t727hxg07vsy28f08!@o2)asfnk^3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG          = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS  = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'content',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF     = 'protoplate.urls'
WSGI_APPLICATION = 'protoplate.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'protobase',
        'USER':     'willemrx' ,
        'PASSWORD': 'root'     ,
        'HOST':     '127.0.0.1',
        'PORT':     '5432'
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_L10N      = True
USE_TZ        = True


# Not sticking with the precooked Django User...

AUTH_USER_MODEL = 'accounts.BespokeUser'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
STATIC_PATH   = os.path.join(BASE_DIR, 'static'   )
MEDIA_ROOT    = os.path.join(BASE_DIR, 'media'    )

STATIC_URL       = '/static/'
MEDIA_URL        = '/media/'
TEMPLATE_DIRS    = (TEMPLATE_PATH,)
STATICFILES_DIRS = (STATIC_PATH,  )


# Email settings for local machine testing...  Set TLS to true
# when the show gets going!

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST    = 'localhost'
EMAIL_PORT    = 1025
EMAIL_USE_TLS = False