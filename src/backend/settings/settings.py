import logging
import os
import sys
from datetime import timedelta
from os.path import abspath, dirname, join

import factory
from django.contrib.admin import ModelAdmin
from django.utils import timezone
from IPython.terminal.interactiveshell import TerminalInteractiveShell
from pytz import timezone as global_timezone

from backend.prompt import BackendPrompt

env = os.environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

APPS_DIR = f"{BASE_DIR}/../apps"

SECRET_KEY = env.get("DJANGO_SECRET_KEY")
DEBUG = env.get("DEBUG", "True") == "True"
DEBUG_SQL = env.get("DEBUG_SQL", "True") == "True"
PRODUCTION = env.get("PRODUCTION", "True") == "True"
ENVIRONMENT = env.get("ENVIRONMENT", "unknown")
WSGI_APPLICATION = "backend.wsgi.application"
ROOT_URLCONF = "backend.urls"

INTERNET_PORT = env.get("INTERNET_PORT", "80")
INTERNAL_DEV_IP = env.get("INTERNAL_DEV_IP", "127.0.0.1")

LANGUAGE_CODE = "es-es"
TIME_ZONE = "Europe/Madrid"
timezone.activate("Europe/Madrid")
USE_I18N = True
USE_L10N = True

SOURCE_ROOT_PATH = env.get("SOURCE_ROOT_PATH", "/src")

STATIC_URL = f"{SOURCE_ROOT_PATH}/static/"
STATIC_ROOT = f"{SOURCE_ROOT_PATH}/static/"
STATICFILES_DIRS = [f"{SOURCE_ROOT_PATH}/backend/static"]
MEDIA_URL = f"{SOURCE_ROOT_PATH}/media/"
MEDIA_ROOT = f"{SOURCE_ROOT_PATH}/media/"
MEDIAFILES_DIRS = [f"{SOURCE_ROOT_PATH}/backend/media"]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

INTERNAL_APPS = [
    "core",
    "social_auth",
    "questions",
]

EXTERNAL_LIBRARIES = [
    "simple_history",
    "debug_toolbar",
    "django_extensions",
    "rest_framework",
    "corsheaders",
    "drf_api_logger",
    "drf_spectacular",
    "rest_framework_simplejwt",
    "axes",
]

BASE_APPS = [
    "jet.dashboard",
    "jet",
    "django.contrib.contenttypes",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
INSTALLED_APPS = INTERNAL_APPS + BASE_APPS + EXTERNAL_LIBRARIES

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "drf_api_logger.middleware.api_logger_middleware.APILoggerMiddleware",
    "axes.middleware.AxesMiddleware",  # Should be the last for axes to render lockout messages
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "axes.backends.AxesBackend",
    "rest_framework.authentication.TokenAuthentication",
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": int(env.get("PASSWORD_MIN_LENGTH", 7)),
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

X_FRAME_OPTIONS = "SAMEORIGIN"

LOCALE_PATHS = ("locale",)

PROJECT_ROOT = dirname(dirname(abspath(__file__)))
SITE_ROOT = dirname(PROJECT_ROOT)
SITE_NAME = env.get("PROJECT_NAME")
SITE_ID = 1

sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, join(SITE_ROOT, "apps"))
sys.path.insert(0, join(SITE_ROOT, "tests"))

global_timezone("Europe/Madrid")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "PAGE_SIZE": 25,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "backend",
    "DESCRIPTION": "",
    "VERSION": env.get("API_VERSION", "1.0.0"),
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": "/api/",
    "ENUM_ADD_EXPLICIT_BLANK_NULL_CHOICE": False,
}

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

DRF_API_LOGGER_DATABASE = True
DRF_API_LOGGER_SIGNAL = True
DRF_API_LOGGER_PATH_TYPE = "ABSOLUTE"
DRF_API_LOGGER_EXCLUDE_KEYS = ["password", "token", "access", "refresh"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env.get("POSTGRES_DB"),
        "USER": env.get("POSTGRES_USER"),
        "PASSWORD": env.get("POSTGRES_PASSWORD"),
        "HOST": env.get("POSTGRES_HOST"),
        "PORT": "",
        "DISABLE_SERVER_SIDE_CURSORS": True,
        "TEST": {
            "NAME": "testing_database",
        },
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[%(asctime)s] %(levelname)s (%(name)s) %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file_main": {
            "level": "INFO",
            "class": "logging.handlers.WatchedFileHandler",
            "filename": os.path.join(LOG_DIR, f'{os.environ.get("PROJECT_NAME")}.log'),
            "formatter": "simple",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file_main"],
            "level": "INFO",
        },
        "django": {
            "handlers": ["console", "file_main"],
            "level": "INFO",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["console", "file_main"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console", "file_main"],
            "level": "INFO",
        },
        "axes.apps": {
            "handlers": ["console", "file_main"],
            "level": "CRITICAL",
        },
        "axes.attempts": {
            "handlers": ["console", "file_main"],
            "level": "CRITICAL",
        },
        "axes.handlers.database": {
            "handlers": ["console", "file_main"],
            "level": "CRITICAL",
        },
    },
}

TerminalInteractiveShell.prompts_class = BackendPrompt
TerminalInteractiveShell.highlighting_style_overrides = BackendPrompt.get_style()

IPYTHON_ARGUMENTS = [
    "--ext",
    "autoreload",
]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

AUTH_USER_MODEL = "core.User"

ACCESS_TOKEN_LIFETIME_MINUTES = int(env.get("ACCESS_TOKEN_LIFETIME_MINUTES", 60))
REFRESH_TOKEN_LIFETIME_DAYS = int(env.get("REFRESH_TOKEN_LIFETIME_DAYS", 7))
SLIDING_TOKEN_LIFETIME_MINUTES = int(env.get("SLIDING_TOKEN_LIFETIME_MINUTES", 60))
SLIDING_TOKEN_REFRESH_LIFETIME_DAYS = int(env.get("SLIDING_TOKEN_REFRESH_LIFETIME_DAYS", 7))
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=REFRESH_TOKEN_LIFETIME_DAYS),
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=SLIDING_TOKEN_LIFETIME_MINUTES),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=SLIDING_TOKEN_REFRESH_LIFETIME_DAYS),
}

ALLOWED_HOSTS = [
    "askmeintense.com",
    "backend.askmeintense.com",
    f"backend.askmeintense.com:{INTERNET_PORT}",
    f"{INTERNAL_DEV_IP}",
    "www.askmeintense.com",
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
]

CORS_ALLOWED_ORIGINS = [
    "http://backend.askmeintense.com",
    "https://backend.askmeintense.com",
    "http://askmeintense.com",
    "https://askmeintense.com",
    "http://www.askmeintense.com",
    "https://www.askmeintense.com",
    f"https://{INTERNAL_DEV_IP}",
    f"http://{INTERNAL_DEV_IP}",
    "http://localhost",
    "http://0.0.0.0",
    "http://localhost:3000",
    "http://0.0.0.0:3000",
    "http://127.0.0.1:3000",
]

CSRF_TRUSTED_ORIGINS = [
    "http://backend.askmeintense.com",
    "https://backend.askmeintense.com",
    "http://askmeintense.com",
    "https://askmeintense.com",
    "http://www.askmeintense.com",
    "https://www.askmeintense.com",
    f"https://{INTERNAL_DEV_IP}",
    f"http://{INTERNAL_DEV_IP}",
    "http://localhost",
    "http://0.0.0.0",
    "http://localhost:3000",
    "http://0.0.0.0:3000",
    "http://127.0.0.1:3000",
]

AXES_ENABLED = True
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = timedelta(minutes=30)  # Period of inactivity to clear failed attempts
AXES_RESET_ON_SUCCESS = True  # a successful login will reset the number of failed logins

GOOGLE_API_KEY = None

factory.Faker._DEFAULT_LOCALE = os.getenv("DEFAULT_LOCALE", "es_ES")  # pylint: disable=W0212

ModelAdmin.list_per_page = 15

if DEBUG:
    import socket  # only if you haven't already imported this

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]

SHELL_PLUS = "ipython"
if DEBUG_SQL:
    SHELL_PLUS_PRINT_SQL = True
    SHELL_PLUS_PRINT_SQL_TRUNCATE = None
SHELL_PLUS_IMPORTS = []

if not PRODUCTION:
    FACTORIES_TO_IMPORT = [
        "from core.factories import *",
        "from questions.factories import *",
    ]
    EXTRAS_TO_IMPORT = []
    SHELL_PLUS_IMPORTS += FACTORIES_TO_IMPORT + EXTRAS_TO_IMPORT

if len(sys.argv) > 1 and sys.argv[1] == "test":
    logging.disable(logging.CRITICAL)
