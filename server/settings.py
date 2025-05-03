import os
from pathlib import Path
from decouple import config, Csv
import structlog
import logging
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

INTERNAL_IPS = [
    '0.0.0.0',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'djoser',
    'corsheaders',
    'django_structlog',
    'drf_standardized_errors',
    'django.contrib.postgres',
    'django_telegram_logging',

    'identity.apps.IdentityConfig',
    'referential.apps.ReferentialConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_structlog.middlewares.RequestMiddleware',
]

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / '/templates/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        'ENGINE': config('POSTGRES_ENGINE'),
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST'),
        'PORT': config('POSTGRES_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

DATETIME_FORMAT = '%Y-%m-%d %H:%M'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = 'static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'identity.User'

if DEBUG is True:
    DRF_STANDARDIZED_ERRORS = {"ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS": True}

    INSTALLED_APPS += [
        'debug_toolbar',
        'nplusone.ext.django',
    ]

    MIDDLEWARE.insert(0, 'nplusone.ext.django.NPlusOneMiddleware')

    MIDDLEWARE += [
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'query_counter.middleware.DjangoQueryCounterMiddleware',
        'querycount.middleware.QueryCountMiddleware',
    ]

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticatedOrReadOnly',
            'rest_framework.permissions.IsAuthenticated',
        ),
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 100,
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ),
        'EXCEPTION_HANDLER': 'drf_standardized_errors.handler.exception_handler',
    }

QUERYCOUNT = {
    'THRESHOLDS': {
        'MEDIUM': 50,
        'HIGH': 200,
        'MIN_TIME_TO_LOG':0,
        'MIN_QUERY_COUNT_TO_LOG':0
    },
    'IGNORE_REQUEST_PATTERNS': [],
    'IGNORE_SQL_PATTERNS': [],
    'DISPLAY_DUPLICATES': None,
    'RESPONSE_HEADER': 'X-DjangoQueryCount-Count'
}

NPLUSONE_LOGGER = logging.getLogger('nplusone')
NPLUSONE_LOG_LEVEL = logging.WARN

# logging----------------------------------------------------------------------

TELEGRAM_LOGGING_TOKEN = config('TELEGRAM_BOT_TOKEN')
TELEGRAM_LOGGING_CHAT = config('TELEGRAM_LOGGING_CHAT')
TELEGRAM_LOGGING_EMIT_ON_DEBUG = config('TELEGRAM_LOGGING_EMIT_ON_DEBUG', cast=bool)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json_formatter':{
            '()': structlog.stdlib.ProcessorFormatter,
            'processor': structlog.processors.JSONRenderer(),
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'json_file': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': 'logs/json.log',
            'formatter': 'json_formatter',
        },
        'telegram': {
            'level': 'ERROR',
            'class': 'django_telegram_logging.handler.TelegramHandler'
        },
    },
    'loggers': {
        'nplusone': {
            'handlers': ['console'],
            'level': 'WARN',
        },
        'django_structlog': {
            "handlers": ["json_file", 'telegram', 'console'],
            "level": "INFO",
        },
        'django': {
            'level': 'ERROR',
            'handlers': ['console', 'telegram']
        }
    },
}

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)


# jwt------------------------------------------------------------------------

ACCESS_TOKEN_LIFETIME = timedelta(minutes=int(config('ACCESS_TOKEN_LIFETIME_MINUTES')))
REFRESH_TOKEN_LIFETIME = timedelta(days=int(config('REFRESH_TOKEN_LIFETIME_DAYS')))

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': ACCESS_TOKEN_LIFETIME,
    'REFRESH_TOKEN_LIFETIME': REFRESH_TOKEN_LIFETIME,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# telegram------------------------------------------------------------------------

TELEGRAM_BOT_NAME = config('TELEGRAM_BOT_NAME')
TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')

# cors------------------------------------------------------------------------

CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', cast=bool)
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=Csv())
DOMAIN = config('FRONT_URL')

# customdjosersettingsforuser-------------------------------------------------------

# DJOSER = {
#     'PASSWORD_RESET_CONFIRM_URL': 'change-password/{uid}/{token}',
#     'PASSWORD_RESET_CONFIRM_RETYPE': True,
#     'HIDE_USERS': False,
#     'PERMISSIONS': {
#         'user_create': ['identity.permissions.IsAdmin'],
#         'user_list': ['identity.permissions.UserPermission'],
#     },
#     'SERIALIZERS': {
#         'password_reset': 'djoser.serializers.SendEmailResetSerializer',
#         'user_create': 'identity.serializers.CustomUserCreateSerializer',
#         'current_user': 'identity.serializers.CustomUserSerializer',
#         'user': 'identity.serializers.CustomUserSerializer',
#     }
# }

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda _request: DEBUG
}

if config('USE_HTTPS', cast=bool):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 60
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    SECURE_SSL_REDIRECT = True
    SECURE_REDIRECT_EXEMPT = [
        '^health/',
    ]
    SECURE_REDIRECT_EXEMPT += config('SECURE_REDIRECT_EXEMPT', cast=Csv())

