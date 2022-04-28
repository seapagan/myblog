"""Django settings for myblog project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)  # loads the configs from .env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read the SECRET_KEY from the .env file
SECRET_KEY = str(os.getenv("SECRET_KEY"))

# Set DEBUG from the .env file
DEBUG = bool(int(os.getenv("DEBUG", 0)))

# Add extra hosts from the .env file if specified
EXTRA_HOSTS = list(filter(None, str(os.getenv("ALLOWED_HOSTS", "")).split(",")))
ALLOWED_HOSTS = ["localhost", "127.0.0.1"] + EXTRA_HOSTS

# Application definition
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "user_sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
    "preferences",
    "rundevserver",
    "compressor",
    "django.forms",
    "django_gravatar",
    "ckeditor",
    "ckeditor_uploader",
    "dj_pagination",
    "maintenance_mode",
    "secretballot",
    "captcha",
    "likes",
    "blog",
    "users",
    "hitcount",
]

# HTML_MINIFY = True

# only include the Admin paths if we are in DEBUG mode
if DEBUG:
    INSTALLED_APPS = ["myblog.apps.MyAdminConfig"] + INSTALLED_APPS

# Change this IF needed AND running the server behind a proxy.
FIX_PROXY_IP = bool(int(os.getenv("FIX_PROXY_IP", 0)))


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # "django.contrib.sessions.middleware.SessionMiddleware",
    "user_sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "maintenance_mode.middleware.MaintenanceModeMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "dj_pagination.middleware.PaginationMiddleware",
    "likes.middleware.SecretBallotUserIpUseragentMiddleware",
    "htmlmin.middleware.HtmlMinifyMiddleware",
    "htmlmin.middleware.MarkRequestMiddleware",
]

# Only load the XForwarded fix if explicitly required
if FIX_PROXY_IP:
    MIDDLEWARE = [
        "x_forwarded_for.middleware.XForwardedForMiddleware"
    ] + MIDDLEWARE


# configure the user_sessions engine
SESSION_ENGINE = "user_sessions.backends.db"
# silence the warning about the session engine, we have a third party one.
SILENCED_SYSTEM_CHECKS = ["admin.E410"]

# location of GeoIP data
GEOIP_PATH = BASE_DIR / "geoip"

ROOT_URLCONF = "myblog.urls"

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
                "maintenance_mode.context_processors.maintenance_mode",
                "django.contrib.messages.context_processors.messages",
                "preferences.context_processors.preferences_cp",
            ],
        },
    },
]

WSGI_APPLICATION = "myblog.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": str(os.getenv("BLOG_DB_NAME")),
        "USER": str(os.getenv("BLOG_DB_USER")),
        "PASSWORD": str(os.getenv("BLOG_DB_PASSWORD")),
        "HOST": str(os.getenv("BLOG_DB_HOST")),
        "PORT": str(os.getenv("BLOG_DB_PORT")),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = "static"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)


MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "blog:index"
LOGOUT_REDIRECT_URL = "blog:index"
LOGIN_URL = "login"

# set a SITE_ID, due to the (3rd party) 'preferences' app using the sites
# functionality. long term, rewrite the addon to remove this need.
SITE_ID = 1

X_FRAME_OPTIONS = "SAMEORIGIN"

# settings for the dj-pagination application.
PAGINATION_DISPLAY_DISABLED_PREVIOUS_LINK = True
PAGINATION_DISPLAY_DISABLED_NEXT_LINK = True
PAGINATION_DEFAULT_WINDOW = 1
PAGINATION_DEFAULT_MARGIN = 0
PAGINATION_INVALID_PAGE_RAISES_404 = True
PAGINATION_DISABLE_LINK_FOR_FIRST_PAGE = True

# settings for dh-hitcount application
HITCOUNT_HITS_PER_IP_LIMIT = 0
HITCOUNT_USE_IP = True

# settings for CKEditor Rich-text editor plugin
CKEDITOR_UPLOAD_PATH = "image/uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_CONFIGS = {
    "default": {},
    "post": {
        "width": "auto",
        "height": "450px",
        "tabSpaces": 4,
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["CodeSnippet"],
            ["Format"],
            [
                "Bold",
                "Italic",
                "Underline",
                "Strike",
                "RemoveFormat",
                "Blockquote",
            ],
            [
                "JustifyLeft",
                "JustifyCenter",
                "JustifyRight",
                "JustifyBlock",
            ],
            ["Smiley", "SpecialChar"],
            ["TextColor", "BGColor"],
            ["Image"],
            ["Link", "Unlink"],
            ["Table", "HorizontalRule"],
            ["NumberedList", "BulletedList"],
            ["Maximize"],
            ["Preview"],
        ],
        "removePlugins": "exportpdf",
        "extraPlugins": ",".join(
            [
                "codesnippet",
                "prism",
                "widget",
                "lineutils",
            ]
        ),
        "format_tags": "p;h2;h3;h4;pre;address;div",
        "editorplaceholder": "Start typing something great!",
    },
    "comment": {
        "width": "auto",
        "height": "450px",
        "tabSpaces": 4,
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["CodeSnippet"],
            ["Format"],
            [
                "Bold",
                "Italic",
                "Underline",
                "Strike",
                "RemoveFormat",
                "Blockquote",
            ],
            ["Smiley", "SpecialChar"],
            ["TextColor"],
            ["Link", "Unlink"],
            ["Table", "HorizontalRule"],
            ["NumberedList", "BulletedList"],
            ["Maximize"],
            ["Preview"],
        ],
        "removePlugins": "exportpdf",
        "extraPlugins": ",".join(
            [
                "codesnippet",
                "prism",
                "widget",
                "lineutils",
            ]
        ),
        "format_tags": "p;h2;h3;h4;pre;address;div",
        "editorplaceholder": "Enter your Comment. Please be polite and thoughtful to others.",
    },
}

# Secret Ballot settings.
SECRETBALLOT_FOR_MODELS = {
    "blog.Blog": {},
}

# Settings for the maintenance_mode plugin
MAINTENANCE_MODE_IGNORE_STAFF = True
MAINTENANCE_MODE_IGNORE_SUPERUSER = True

# recapcha settings
RECAPTCHA_PUBLIC_KEY = str(os.getenv("RECAPTCHA_PUBLIC_KEY"))
RECAPTCHA_PRIVATE_KEY = str(os.getenv("RECAPTCHA_PRIVATE_KEY"))

# rundevserver settings
RDS_ALL_INTERFACES = True
RDS_DEBUG = True
