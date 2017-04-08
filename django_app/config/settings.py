"""
Django settings for record project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
import json
import os

DEBUG = os.environ.get('MODE') == 'DEBUG'
STORAGE_S3 = os.environ.get('STORAGE') == 'S3' or DEBUG is False
# DB_RDS = os.environ.get('DB') == 'RDS'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
CONF_DIR = os.path.join(ROOT_DIR, '.conf-secret')

# Config File Settings
config_file_name = 'conf-local.json' if DEBUG else 'conf-deploy.json'
CONFIG_COMMON_FILE = json.loads(open(os.path.join(CONF_DIR, 'conf-common.json')).read())
CONFIG_FILE = json.loads(open(os.path.join(CONF_DIR, config_file_name)).read())

for key, key_dict in CONFIG_COMMON_FILE.items():
    if not CONFIG_FILE.get(key):
        CONFIG_FILE[key] = {}
    for inner_key, inner_key_dict in key_dict.items():
        CONFIG_FILE[key][inner_key] = inner_key_dict

# TEMPLATES
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# STATIC
STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# FRONT
FRONT_URL = '/front/'
FRONT_DIR = os.path.join(BASE_DIR, 'front')

STATICFILES_DIRS = [
    STATIC_DIR,
    FRONT_DIR,
]

# AWS S3 Setting
AWS_ACCESS_KEY_ID = CONFIG_FILE['aws']['access_key_id']
AWS_SECRET_ACCESS_KEY = CONFIG_FILE['aws']['secret_access_key']

AWS_S3_HOST = '{}.s3.amazonaws.com'.format(CONFIG_FILE['aws']['s3_region'])
AWS_S3_SIGNATURE_VERSION = CONFIG_FILE['aws']['s3_signature_version']
AWS_STORAGE_BUCKET_NAME = CONFIG_FILE['aws']['s3_storage_bucket_name']
AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)

if STORAGE_S3:
    # S3 Static Settings
    STATICFILES_STORAGE = 'config.storages.StaticStorage'
    STATICFILES_LOCATION = 'static'
    STATIC_URL = 's3.{custom_domain}.amazonaws.com/{staticfiles_location}/'.format(
        custom_domain=AWS_S3_CUSTOM_DOMAIN,
        staticfiles_location=STATICFILES_LOCATION
    )
    # S3 Media Settings
    DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'
    MEDIAFILES_LOCATION = 'media'
    MEDIA_URL = 's3.{custom_domain}.amazonaws.com/{mediafiles_location}/'.format(
        custom_domain=AWS_S3_CUSTOM_DOMAIN,
        mediafiles_location=MEDIAFILES_LOCATION,
    )
    # S3 front Settings
    DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'
    FRONTFILES_LOCATION = 'front'
    FRONT_URL = 's3.{custom_domain}.amazonaws.com/{frontfiles_location}/'.format(
        custom_domain=AWS_S3_CUSTOM_DOMAIN,
        frontfiles_location=FRONTFILES_LOCATION,
    )
else:
    STATIC_ROOT = os.path.join(ROOT_DIR, 'static_root')
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG_FILE['django']['secret-key']

ALLOWED_HOSTS = CONFIG_FILE['django']['allowed-hosts']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'storages',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'user',
    'diary',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATE_DIR
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': CONFIG_FILE['db']['ENGINE'],
        'NAME': CONFIG_FILE['db']['NAME'],
        'USER': CONFIG_FILE['db']['USER'],
        'PASSWORD': CONFIG_FILE['db']['PASSWORD'],
        'HOST': CONFIG_FILE['db']['HOST'],
        'PORT': CONFIG_FILE['db']['PORT']
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'user.Member'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
