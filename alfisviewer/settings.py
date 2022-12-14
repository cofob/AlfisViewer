from pathlib import Path
from json import load as json_load
import subprocess
from secrets import token_hex
import os

try:
    COMMIT_HASH = (
        subprocess.check_output("git rev-parse --short HEAD".split(" "))
        .decode()
        .replace("\n", "")
        .upper()
    )
except FileNotFoundError:
    COMMIT_HASH = token_hex(3).upper()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


with open("config.json", "r") as file:
    CONFIG = json_load(file)


if not os.path.isdir(str(BASE_DIR / "logs")):
    os.mkdir(str(BASE_DIR / "logs"))

LOGGING = CONFIG.get(
    "LOGGING",
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {message}",
                "style": "{",
            },
            "simple": {
                "format": "{levelname} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "file": {
                "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
                "class": "logging.FileHandler",
                "filename": str(BASE_DIR / "logs" / "django.txt"),
                "formatter": "verbose",
            },
            "console": {"class": "logging.StreamHandler", "formatter": "simple"},
        },
        "loggers": {
            "django": {
                "handlers": ["file", "console"],
                "level": "WARN",
                "propagate": True,
            },
        },
    },
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG["DEBUG"]

ALLOWED_HOSTS = CONFIG["ALLOWED_HOSTS"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "index.apps.IndexConfig",
    "block.apps.BlockConfig",
    "domain.apps.DomainConfig",
    "search.apps.SearchConfig",
    "key.apps.KeyConfig",
    "alfisviewer.lib",
    "settings_app.apps.SettingsAppConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "alfisviewer.urls"

TEMPLATE_DIRS = [
    BASE_DIR / "templates",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": TEMPLATE_DIRS,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "alfisviewer.lib.context_processors.commit_hash",
                "alfisviewer.lib.context_processors.block_count",
                "alfisviewer.lib.context_processors.domain_count",
                "alfisviewer.lib.context_processors.update_scheduler",
            ],
        },
    },
]

WSGI_APPLICATION = "alfisviewer.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

LANGUAGES = (
    ("en", "English"),
    ("ru", "Russian"),
)

LANGUAGE_CODES = ("en", "ru")

# Locale files folder
LOCALE_PATHS = (BASE_DIR / "locale",)

TIME_ZONE = "UTC"

USE_I18N = True

LANGUAGE_COOKIE_NAME = "lang"

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = CONFIG.get("STATIC_ROOT")

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
