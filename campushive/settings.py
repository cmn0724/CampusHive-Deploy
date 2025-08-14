# campushive/settings.py
from pathlib import Path
from decouple import config, Csv
import dj_database_url
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Deployment-Ready Settings ---
# SECRET_KEY, DEBUG, and ALLOWED_HOSTS will be read from environment variables.
# For local development, create a .env file in the project root.
# For production (e.g., AWS), these will be set in the server environment.
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # My apps
    'users.apps.UsersConfig',
    'courses.apps.CoursesConfig',
    'equipment.apps.EquipmentConfig',
    'venues.apps.VenuesConfig', 
    # Third-party apps
    'django_filters',
    'crispy_forms',
    'crispy_bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise middleware should be placed right after SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'campushive.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'campushive.wsgi.application'


# --- Database ---
# Uses dj_database_url to parse the DATABASE_URL environment variable.
# Falls back to local SQLite for simple local setup if DATABASE_URL is not set.
# default_db_url = 'sqlite:///' + str(BASE_DIR / 'db.sqlite3')
# DATABASES = {
#     'default': dj_database_url.config(default=default_db_url)
# }
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# --- 关键修复：为 psycopg v3 强制使用新的数据库引擎 ---
# 当检测到数据库是 postgresql 时 (在 Elastic Beanstalk 环境中，DATABASE_URL 会被设置)
# dj_database_url 可能会默认设置为旧的 psycopg2 引擎，我们需要手动覆盖它。
# if DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
#    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True


# --- Static files (CSS, JavaScript, Images) ---
# STATIC_URL = 'static/'
STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / 'static']
# This is where collectstatic will gather all static files for production.
# STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_ROOT = BASE_DIR / 'static'

# WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# --- Media files (User-uploaded content) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- Custom User Model & Auth URLs ---
AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'


# --- Crispy Forms ---
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# --- Production Security Settings ---
# In production (when DEBUG=False), these settings will be applied.
if not DEBUG:
    # CSRF_COOKIE_SECURE = True
    # SESSION_COOKIE_SECURE = True
    # SECURE_SSL_REDIRECT = True
    # SECURE_HSTS_SECONDS = 31536000  # 1 year
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True
    pass