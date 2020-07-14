import os
import sentry_sdk
import pydash as _
from core import get_env, get_env_bool
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APP_VERSION = '1.0.0'

APP_NAME = get_env('APP_NAME', 'Application')

APP_URL = get_env('APP_URL', 'http://localhost')

SECRET_KEY = get_env('APP_KEY', 'somerandomstring')

DEBUG = get_env_bool('APP_DEBUG')

AUTH_USER_MODEL = 'common.User'

ALLOWED_HOSTS = [
    '*'
]

INTERNAL_IPS = [
    '127.0.0.1',
]

LOGIN_URL = '/login'

APPEND_SLASH = False


# SSL Configuration
SECURE_SSL_REDIRECT = get_env_bool('FORCE_HTTPS', None)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Celery
CELERY_ENABLE_UTC = True

CELERY_TIMEZONE = 'Asia/Jakarta'

CELERY_RESULT_BACKEND = 'django-db'

CELERY_BROKER_TRANSPORT_OPTIONS = {
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 0.5,
    'interval_max': 3,
}


# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'common.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'debug': '1000/second',
    }
}


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fullurl',
    'debug_toolbar',
    'django_celery_results',
    'rest_framework',
    'corsheaders',
    'oauth2_provider',

    'softdelete',
    'common',
    'app',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'common.middleware.HttpRequestPatchMiddleware',
    'common.middleware.ServiceProviderMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.PreviousUrlMiddleware',
    'common.middleware.HandleValidationErrorsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATE_LOADERS = [
    'core.template.loaders.filesystem.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # Project specific
                'core.context_processors.settings_context_processor',
                'common.context_processors.common_context_processor',
            ],
            'builtins': [
                'common.templatetags.builtins',
            ],
            'loaders': [('django.template.loaders.cached.Loader', TEMPLATE_LOADERS)] if not DEBUG else TEMPLATE_LOADERS,
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASE_ENGINES = {
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env('DB_NAME', 'django'),
        'USER': get_env('DB_USERNAME', 'root'),
        'PASSWORD': get_env('DB_PASSWORD', ''),
        'HOST': get_env('DB_HOST', '127.0.0.1'),
        'PORT': get_env('DB_PORT', '3306'),
    },
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': get_env('DB_NAME', os.path.join(BASE_DIR, 'database.sqlite')),
        'OPTIONS': {},
    }
}

DATABASES = {
    'default': DATABASE_ENGINES[get_env('DB_ENGINE', 'mysql')]
}


# Cache
CACHE_BACKENDS = {
    'memory': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'KEY_PREFIX': _.slugify(APP_NAME, '_') + '_cache',
    },
    'redis': {
        'BACKEND': 'redis_cache.RedisCache',
        'KEY_PREFIX': _.slugify(APP_NAME, '_') + '_cache',
        'LOCATION': [
            '%s:%s' % (get_env('REDIS_HOST', '127.0.0.1'), get_env('REDIS_PORT', 6379)),
        ],
        'OPTIONS': {
            'DB': int(get_env('REDIS_CACHE_DB', 1)),
            'PASSWORD': get_env('REDIS_PASSWORD'),
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            },
            'MAX_CONNECTIONS': 1000,
        }
    }
}

CACHES = _.merge({
    'default': CACHE_BACKENDS[get_env('CACHE_BACKEND', 'memory')]
}, CACHE_BACKENDS)


# Emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_env('MAIL_HOST', '127.0.0.1')
EMAIL_HOST_USER = get_env('MAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env('MAIL_HOST_PASSWORD')
EMAIL_PORT = int(get_env('MAIL_PORT', 1025))
EMAIL_USE_TLS = get_env_bool('MAIL_USE_TLS')
EMAIL_FROM_ADDRESS = get_env('MAIL_FROM_ADDRESS', 'info@example.com')
EMAIL_FROM_NAME = get_env('MAIL_FROM_NAME', 'Support')
DEFAULT_FROM_EMAIL = '%s <%s>' % (EMAIL_FROM_NAME, EMAIL_FROM_ADDRESS)
EMAIL_SUBJECT_PREFIX = get_env('MAIL_SUBJECT_PREFIX', '[%s] ' % APP_NAME)


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'datetime': {
            'format': '[{asctime}] {levelname}: {message}',
            'style': '{',
        }
    },
    'handlers': {
        'file': {
            'level': get_env('LOG_LEVEL', 'INFO'),
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'formatter': 'datetime',
            'when': 'MIDNIGHT',
            'interval': 1,
        },
        'behave-file': {
            'level': get_env('LOG_LEVEL', 'INFO'),
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/behave.log'),
            'formatter': 'datetime',
        },
        'console': {
            'level': get_env('LOG_LEVEL', 'INFO'),
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'behave': {
            'handlers': ['behave-file'],
            'level': get_env('LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'django': {
            'handlers': [get_env('LOG_HANDLER', 'file'), 'mail_admins'],
            'level': get_env('LOG_LEVEL', 'INFO'),
        },
        'django-file': {
            'handlers': ['file'],
            'level': get_env('LOG_LEVEL', 'INFO'),
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Debug Toolbar
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'common.middleware.show_toolbar',
}

DISABLE_DEBUG_TOOLBAR = get_env_bool('DISABLE_DEBUG_TOOLBAR')


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'id'

FAKER_LOCALE = 'id'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = get_env('STATIC_URL', '/static/')

MEDIA_URL = get_env('MEDIA_URL', '/media/')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'public/static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'public/dist')

MEDIA_ROOT = os.path.join(BASE_DIR, 'public/media')


sentry_sdk.init(
    dsn=get_env('SENTRY_DSN'),
    integrations=[DjangoIntegration(), CeleryIntegration()]
)
