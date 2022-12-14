"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=False)

ENV = os.environ["RELEASE_STAGE"]
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-vwh6ab#bd3c5-%&zf%o%6m%i7i23y-_5nhpt3&u@4vdu+k=o8@"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV == "dev"
ROLE = os.environ["ROLE"]

HOST_IP = os.environ.get("HOST_IP", "localhost")

ALLOWED_HOSTS = [
    "0.0.0.0",
    "localhost",
    "storyworx.co",
    "api.storyworx.co",
    "payment-processor-service",
    "payment-processor-stripe-worker-service",
    "payment-processor-service.apps",
    "payment-processor-stripe-worker-service.apps",
    os.environ.get("HOST_IP"),
    os.environ.get("POD_IP"),
]

HEALTHCHECK_APPS = []
# Application definition
if ROLE == "app":
    HEALTHCHECK_APPS = [
        "health_check",
        "health_check.db",
        "health_check.contrib.redis",
        "health_check.contrib.celery",
        "health_check.contrib.celery_ping",
    ]
elif ROLE == "runner":
    HEALTHCHECK_APPS = [
        "health_check",
        "health_check.db",
        "health_check.contrib.redis",
        "health_check.contrib.celery",
        "health_check.contrib.celery_ping",
    ]
elif ROLE == "worker":
    HEALTHCHECK_APPS = [
        "health_check.contrib.celery",
        "health_check.contrib.celery_ping",
    ]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    "drf_spectacular",
    "core",
    "api",
    "payment_processor",
    "rest_framework",
    "django_prometheus",
] + HEALTHCHECK_APPS

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "core.middlewares.HealthCheckMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ["MYSQL_DATABASE"],
        "USER": os.environ["MYSQL_USER"],
        "PASSWORD": os.environ["MYSQL_PASSWORD"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ["DB_PORT"],
        "OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "root": {
            "format": "{levelname} {message}",
            "style": "{",
        },
        # "verbose": {
        #     "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
        #     "style": "{",
        # },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "root",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = "static/"
if ENV == "dev":
    STATICFILES_DIRS = (STATIC_URL,)
elif ENV == "prod":
    STATIC_ROOT = os.path.join(BASE_DIR, "static")


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Payment processor API",
    "DESCRIPTION": "Payment processing microservice handles transactions",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "PREPROCESSING_HOOKS": ["core.utils.spectacular_hooks.preprocessing_filter_spec"],
    # OTHER SETTINGS
}

# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
#         "LOCATION": "127.0.0.1:11211",
#     }
# }


REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:6379"
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_IMPORTS = ("payment_processor.tasks",)

KAFKA_HOST = os.environ.get("KAFKA_HOST")
