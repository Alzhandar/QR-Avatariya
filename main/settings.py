import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '87.255.198.245',
    'oyster-app-auigo.ondigitalocean.app',
    '0.0.0.0',
]

CSRF_TRUSTED_ORIGINS = [
    'https://oyster-app-auigo.ondigitalocean.app',
    'http://oyster-app-auigo.ondigitalocean.app',
    'http://87.255.198.245',
]

CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS
CORS_ALLOW_CREDENTIALS = True

AVATARIYA_BASE_URL = os.getenv('AVATARIYA_BASE_URL', 'http://127.0.0.1:7654')
address_for_qr = AVATARIYA_BASE_URL
allow_hosts = os.getenv('ALLOW_HOSTS', '').split(',') if os.getenv('ALLOW_HOSTS') else []
hosts = os.getenv('HOSTS', '').split(',') if os.getenv('HOSTS') else []
instagram = os.getenv('INSTAGRAM_URL', '')
whatsapp = os.getenv('WHATSAPP_URL', '')
menu_kz = os.getenv('MENU_KZ_URL', '')
menu_ru = os.getenv('MENU_RU_URL', '')
pay = ''

from_1c_server = os.getenv('FROM_1C_SERVER', '')
from_1c_username = os.getenv('FROM_1C_USERNAME', '')
from_1c_password = os.getenv('FROM_1C_PASSWORD', '')

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
]

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

WSGI_APPLICATION = 'main.wsgi.application'


"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'NAME': os.getenv('DB_NAME', 'mydb'),
        'USER': os.getenv('DB_USER', 'myuser'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'mypassword'),
    }
}
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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


LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Asia/Almaty'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# SESSION_COOKIE_AGE = 1209600               # 2 недели
# SESSION_SAVE_EVERY_REQUEST = True      
# SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# SESSION_COOKIE_SECURE = not DEBUG        
# CSRF_COOKIE_SECURE = not DEBUG

# Если надо:
# SESSION_COOKIE_DOMAIN = '.oyster-app-auigo.ondigitalocean.app'
# SESSION_COOKIE_SAMESITE = None

# -----------------------------------------------------------------------------
# Рекомендуется в продакшене включать заголовки HSTS (HTTP Strict Transport Security)
# -----------------------------------------------------------------------------
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# -----------------------------------------------------------------------------