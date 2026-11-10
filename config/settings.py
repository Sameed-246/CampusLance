from pathlib import Path
from dotenv import load_dotenv
import os


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# Load variables from .env
load_dotenv(BASE_DIR / ".env")


# ============================================================
# API KEYS
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = "django-insecure-campuslance-development-key-change-this"

DEBUG = True


# ============================================================
# ALLOWED HOSTS
# ============================================================

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "10.108.175.42",
]


# ============================================================
# CSRF TRUSTED ORIGINS
# Required when testing Django from your phone
# over the same Wi-Fi/network.
# ============================================================

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://10.108.175.42:8000",
]


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [

    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # CampusLance apps
    "accounts",
    "jobs",
    "applications",
    "dashboard",
    "profiles",
    "messaging",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# URL CONFIGURATION
# ============================================================

ROOT_URLCONF = "config.urls"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [

    {
        "BACKEND":
            "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {

            "context_processors": [

                # Django request
                "django.template.context_processors.request",

                # Authentication / user
                "django.contrib.auth.context_processors.auth",

                # Django messages
                "django.contrib.messages.context_processors.messages",

                # ====================================================
                # CAMPUSLANCE UNREAD MESSAGE NOTIFICATION
                # Provides:
                # {{ unread_message_count }}
                # to every template.
                # ====================================================

                "messaging.context_processors.unread_messages",

            ],
        },
    },
]


# ============================================================
# WSGI
# ============================================================

WSGI_APPLICATION = "config.wsgi.application"


# ============================================================
# DATABASE
# Use MySQL when the project is configured for it, otherwise
# fall back to SQLite so local development works without a
# database server running.
# ============================================================

DB_ENGINE = os.getenv("DB_ENGINE", "sqlite").lower()

if DB_ENGINE == "mysql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("DB_NAME", "campuslance_db"),
            "USER": os.getenv("DB_USER", "root"),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "3306"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME":
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation.MinimumLengthValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation.CommonPasswordValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ============================================================
# LANGUAGE & TIME
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# ============================================================
# MEDIA FILES
# ============================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================================
# CUSTOM USER MODEL
# ============================================================

AUTH_USER_MODEL = "accounts.CustomUser"


# ============================================================
# LOGIN / LOGOUT REDIRECTS
# ============================================================

LOGIN_URL = "/login/"

LOGIN_REDIRECT_URL = "/jobs/"

LOGOUT_REDIRECT_URL = "/login/"


# ============================================================
# EMAIL
# ============================================================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"