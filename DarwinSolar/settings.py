"""
Django settings for DarwinSolar project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# import e4sk as k


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
# amazon SES Workmail setting
#
# EMAIL_BACKEND = k.EMAIL_BACKEND
# AWS_ACCESS_KEY_ID = k.AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY = k.AWS_SECRET_ACCESS_KEY
# AWS_SES_REGION_NAME = k.AWS_SES_REGION_NAME
# AWS_SES_REGION_ENDPOINT = k.AWS_SES_REGION_ENDPOINT
#
# # Aws s3 storage config
# AWS_STORAGE_BUCKET_NAME = k.AWS_STORAGE_BUCKET_NAME
# DEFAULT_FILE_STORAGE = k.DEFAULT_FILE_STORAGE
# AWS_S3_FILE_OVERWRITE = True
# AWS_DEFAULT_ACL = None
# STATICFILES_STORAGE = k.STATICFILES_STORAGE
# AWS_S3_CUSTOM_DOMAIN = k.AWS_S3_CUSTOM_DOMAIN
AWS_STORAGE_BUCKET_NAME = 'darwinsolar-bucket'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

DEBUG = True
# if DEBUG:
#     EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = k.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = ['*', ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # my app
    'ds',
    'accounts',
    'customer_portal',
    'company',
    'rest_framework',
    'rest_framework.authtoken',
    'stats',
    'corsheaders',
    'django_rest_passwordreset',
    # 'django- storages',
    'storages',
]
AUTH_USER_MODEL = 'accounts.CustomUser'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        # 'company.api.installer_api.authentication.InstallerTokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ]
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # cors header added for allowing cors

]

PASSWORD_RESET_TIMEOUT = 86400

# added for cors management
CORS_ALLOW_ALL_ORIGINS = True  # If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://www.darwin.solar',
]  # If this is used, then not need to use `CORS_ALLOW_ALL_ORIGINS = True`
CORS_ALLOWED_ORIGIN_REGEXES = [
    'http://localhost:3000',
    'https://www.darwin.solar',
]
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
# added for cors management
ROOT_URLCONF = 'DarwinSolar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'DarwinSolar.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# this is for local server sqlite3 django
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# this is for aws server mysql

# DATABASES = {
#     'default': {
#         # 'ENGINE': 'django.db.backends.mysql',
#         'ENGINE': 'mysql.connector.django',
#         'NAME': k.DB_NAME,
#         'USER': k.DB_USER,
#         'PASSWORD': k.DB_PASSWORD,
#         'HOST': k.DB_HOST,
#         'PORT': 3306
#     }
# }

#  this is for local server mysql

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.mysql',
        'ENGINE': 'mysql.connector.django',
        'NAME': 'e4solar',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': 3306
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Australia/Darwin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')  # for production
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/')]  # for development

MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
