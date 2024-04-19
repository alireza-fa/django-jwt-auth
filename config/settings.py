"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+c(98bt)x$hbm29n#vi_x+u$tcnq*l6q2up*wvl+m3=-dtzlr0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Local apps
    'd_jwt_auth.apps.DJwtAuthConfig',
    # Third party apps
    'drf_spectacular',
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

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# DRF
REST_FRAMEWORK = {
    # YOUR SETTINGS
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'd_jwt_auth.authenticate.JWTAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


# Spectacular
SPECTACULAR_SETTINGS = {
    'TITLE': 'Django Jwt Auth',
    'DESCRIPTION': 'django-jwt-auth is an application for authenticating users with jwt in Django with very high'
                   ' security and practical features',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': True,
    # OTHER SETTINGS
    'PLUGINS': [
        'drf_spectacular.plugins.AuthPlugin',
    ],
    # 'SERVE_PERMISSIONS': ['rest_framework.permissions.IsAdminUser'],
    # Auth with session only in docs without effect to api
    'SERVE_AUTHENTICATION': ["rest_framework.authentication.SessionAuthentication",
                             "rest_framework_simplejwt.authentication.JWTAuthentication"],
}

# CACHE
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis"
                    "://127.0.0.1:6379",
        # "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# JWT AUTH
IP_ADDRESS = "ip_address"
DEVICE_NAME = "device_name"
USER_ID = "id"
USERNAME = "username"
EMAIL = "email"
IS_ACTIVE = "is_active"
IS_STAFF = "is_staff"

JWT_AUTH_REFRESH_TOKEN_CLAIMS = {
    USER_ID: 0,
}

JWT_AUTH_ACCESS_TOKEN_CLAIMS = {
    USER_ID: 0,
    USERNAME: "",
    EMAIL: "",
    IS_ACTIVE: False,
    IS_STAFF: False,
}

JWT_AUTH_ACCESS_TOKEN_USER_FIELD_CLAIMS = {
    USER_ID: 0,
    USERNAME: "",
    EMAIL: "",
    IS_ACTIVE: False,
    IS_STAFF: False,
}

JWT_AUTH_CACHE_USING = True

JWT_AUTH_GET_USER_BY_ACCESS_TOKEN = True

JWT_AUTH_ENCRYPT_KEY = b'\xcaN\x9cO\xf4B\xe8\xb2+\xea\xdbh--6\xd7\xf5u\x18\x9f\x0c\xa5\xf0\xe9\xd6\x8aQ\xe2\xafp\xf8\xff'
