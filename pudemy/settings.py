import os
from datetime import timedelta
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY", default=get_random_secret_key())
DEBUG = os.getenv("DEBUG", default="False").lower() == "true"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", default="*").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_yasg",
    "corsheaders",
    "lms.apps.LmsConfig",
    "users.apps.UsersConfig",
    "api.apps.ApiConfig",
    "payments.apps.PaymentsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pudemy.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "pudemy.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "test_db"),
        "USER": os.getenv("DB_USER", "test_user"),
        "PASSWORD": os.getenv("DB_PASSWORD", "test_user"),
        "HOST": os.getenv("DB_HOST", ""),
        "PORT": os.getenv("DB_PORT", 5432),
    },
    "sqlite3": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

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

LANGUAGE_CODE = "ru-RU"
TIME_ZONE = "Asia/Yekaterinburg"
USE_I18N = True
USE_TZ = True

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

STATIC_URL = "/static/"
STATIC_FILES_DIRS = [BASE_DIR / "static"]
# STATIC_ROOT = BASE_DIR / "static"

AUTH_USER_MODEL = "users.User"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

PAGE_SIZE = 25
COURSE_PAGE_SIZE = 10
LESSON_PAGE_SIZE = 15
MAX_PAGE_SIZE = 100
PAGE_SIZE_QUERY_PARAM = "page_size"


REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_PAGINATION_CLASS": "api.pagination.DefaultPagination",
    "PAGE_SIZE": PAGE_SIZE,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
]

CORS_ALLOW_ALL_ORIGINS = False
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
