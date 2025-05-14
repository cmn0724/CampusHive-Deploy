from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jm)@4f-oyed#b2_l6227zkjde2s+rtmo5d_t9f_fzjj7v@&=l7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # My apps
    'users.apps.UsersConfig',         # 或者直接 'users'
    'courses.apps.CoursesConfig',     # 或者直接 'courses'
    'equipment.apps.EquipmentConfig', # 或者直接 'equipment's
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'campushive.urls'

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # 或者 Django 默认的 BASE_DIR
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True, # 允许Django也会在每个app内的'templates'文件夹中查找模板
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


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

# USE_I18N = True

# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
# 告诉 Django 在哪里查找项目级别的静态文件 (除了每个 app 下的 'static/' 目录)

STATICFILES_DIRS = [
    BASE_DIR / 'static', # 指向项目根目录 (与 manage.py 同级) 下的 'static' 文件夹
]

# STATIC_ROOT = BASE_DIR / 'staticfiles' # (可选) collectstatic 命令会将所有静态文件收集到这个目录，主要用于生产环境部署
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # 初始阶段使用 SQLite
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    # 如果想立即使用 PostgreSQL (确保服务已启动且数据库已创建):
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'campushive_db',       # 数据库名
    #     'USER': 'your_db_user',       # 数据库用户名
    #     'PASSWORD': 'your_db_password', # 数据库密码
    #     'HOST': 'localhost',          # 数据库服务器地址
    #     'PORT': '5432',               # PostgreSQL 默认端口
    # }
}

LANGUAGE_CODE = 'en-us' # 或者 'zh-hans' 如果你想界面默认为中文
TIME_ZONE = 'Asia/Shanghai' # 设置为你的时区
USE_I18N = True
USE_TZ = True

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# Login/Logout URLs
LOGIN_REDIRECT_URL = 'home'  # Name of the URL pattern for the homepage/dashboard, 登录后重定向的URL名称
LOGOUT_REDIRECT_URL = 'home' # Or 'login' if you prefer(登出后重定向的 URL 名称 (或者 'login' 如果你希望用户登出后返回登录页))
LOGIN_URL = 'login'          # Default is '/accounts/login/'(登录页面的 URL 名称 (如果未登录用户访问需登录页面时，会重定向到这里))