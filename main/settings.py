"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os 
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '87.255.198.245',
    'whale-app-iepuq.ondigitalocean.app',
    '0.0.0.0',
]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'restaurant',
    'administrator',
    'corsheaders',
    'storages'
]

AWS_ACCESS_KEY_ID = os.getenv('DO_SPACES_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('DO_SPACES_SECRET')
AWS_STORAGE_BUCKET_NAME = os.getenv('DO_SPACES_BUCKET')
AWS_S3_ENDPOINT_URL = os.getenv('DO_SPACES_ENDPOINT')
AWS_S3_REGION_NAME = os.getenv('DO_SPACES_REGION')

AWS_DEFAULT_ACL = 'public-read'
AWS_S3_USE_SSL = True
AWS_S3_VERIFY = True
AWS_S3_ADDRESSING_STYLE = 'virtual'
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_REGION_NAME}.digitaloceanspaces.com/'
MEDIA_ROOT = 'media/'

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AVATARIYA_BASE_URL = os.getenv('AVATARIYA_BASE_URL')
address_for_qr = AVATARIYA_BASE_URL
allow_hosts = os.getenv('ALLOW_HOSTS').split(',')
hosts = os.getenv('HOSTS').split(',')
instagram = os.getenv('INSTAGRAM_URL')
whatsapp = os.getenv('WHATSAPP_URL')
menu_kz = os.getenv('MENU_KZ_URL')
menu_ru = os.getenv('MENU_RU_URL')
pay = ''
FEEDBACK = os.getenv('FEEDBACK')
from_1c_server = os.getenv('FROM_1C_SERVER')
from_1c_username = os.getenv('FROM_1C_USERNAME')
from_1c_password = os.getenv('FROM_1C_PASSWORD')
IIKO_WAITER_API_KEY = os.getenv('IIKO_WAITER_API_KEY')
IIKO_WAITER_API_URL = os.getenv('IIKO_WAITER_API_URL')

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
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

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'defaultdb'),
        'USER': os.getenv('DB_USER', 'doadmin'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '25060'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Asia/Almaty'  
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CSRF_TRUSTED_ORIGINS = [
    'https://whale-app-iepuq.ondigitalocean.app',
    'http://whale-app-iepuq.ondigitalocean.app',
    'http://87.255.198.245',
    'http://localhost:7654',
]

CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True

# REDIS_HOST = os.getenv('REDIS_HOST')
# REDIS_PORT = int(os.getenv('REDIS_PORT'))
# REDIS_USER = os.getenv('REDIS_USER')
# REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
# REDIS_DB = int(os.getenv('REDIS_DB'))

# REDIS_SSL = True  
# REDIS_URL = f"rediss://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": REDIS_URL,
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             "CONNECTION_POOL_KWARGS": {
#                 "ssl_cert_reqs": None,  
#                 "retry_on_timeout": True,
#                 "max_connections": 50,
#                 "socket_timeout": 5,
#                 "socket_connect_timeout": 5,
#             },
#             "REDIS_CLIENT_KWARGS": {
#                 "ssl": True,
#                 "ssl_cert_reqs": None,
#             }
#         }
#     }
# }

# DJANGO_REDIS_IGNORE_EXCEPTIONS = True
# DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "retry_on_timeout": True,
                "max_connections": 50,
                "socket_timeout": 5,
                "socket_connect_timeout": 5,
            }
        }
    }
}

DJANGO_REDIS_IGNORE_EXCEPTIONS = True
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True

IIKO_API_LOGIN = os.getenv('IIKO_API_LOGIN')
IIKO_API_TIMEOUT = int(os.getenv('IIKO_API_TIMEOUT', 30))
IIKO_TOKEN_CACHE_KEY = 'iiko_token'
IIKO_TOKEN_CACHE_TIMEOUT = 3600  

IIKO_DEFAULT_WAITER_ID = os.getenv('IIKO_DEFAULT_WAITER_ID')



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'restaurant': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}