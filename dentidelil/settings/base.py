# flake8: noqa
"""
Django settings for dentidelil project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
from sys import path
from pathlib import Path
from storages.backends.azure_storage import AzureStorage

BASE_DIR = Path(__file__).resolve().parent.parent


import environ
env = environ.Env()

# Absolute filesystem path to the top-level project folder:

root = environ.Path(__file__) - 3
PROJECT_ROOT = root()


environ.Env.read_env(root('.env'))

# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = root.path('dentidelil')

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# Do not set SECRET_KEY or LDAP password or any other sensitive data here.

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', True)

ALLOWED_HOSTS = ['localhost','beyondclinic.online','127.0.0.1','tr.localhost']

AZURE_TRANSLATOR_KEY = '106c8f6b95a4460fae580599a6c74348d746'
AZURE_TRANSLATOR_ENDPOINT = 'https://api.cognitive.microsofttranslator.com/'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'compressor',
    'taggit',
    'modelcluster',

    'foundation_formtags',
    'storages',
    'blog',
    'contact',
    'documents_gallery',
    'gallery',
    'pages',
    'people',
    'products',
    'search',
    'users',
    'utils',
    'wagtail.contrib.routable_page',
    'wagtail.contrib.sitemaps',
    'wagtail.contrib.search_promotions',
    'wagtail.search.backends.database',
    'wagtail.contrib.settings',
    "wagtail_localize",
    "wagtail_localize.locales",
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.modeladmin',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtailmedia',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail_feeds',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.linkedin',

)

MIDDLEWARE = (
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sites.middleware.CurrentSiteMiddleware',
  'django.middleware.locale.LocaleMiddleware',  # should be after SessionMiddleware and before CommonMiddleware
  'wagtail.contrib.redirects.middleware.RedirectMiddleware',

)


ROOT_URLCONF = 'dentidelil.urls'

#Admins see https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ("""lotfikanouni""", 'lotfikanouni4@gmail.com'),
)

MANAGERS = ADMINS

ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True

ROSETTA_MESSAGES_PER_PAGE = 500

AZURE_CLIENT_SECRET = 'f0ab28fa69a04f979d904943643d3265'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtail.contrib.settings.context_processors.settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'dentidelil.wsgi.application'

# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------

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

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Some really nice defaults
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'account_login'

ACCOUNT_ALLOW_REGISTRATION = env.bool('DJANGO_ACCOUNT_ALLOW_REGISTRATION', True)
ACCOUNT_ADAPTER = 'users.adapters.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'users.adapters.SocialAccountAdapter'

ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'

# Select the correct user model
AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'account_login'

WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'wagtail.admin.rich_text.HalloRichTextArea'
    }
}

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(root('db.sqlite3')),  # or just 'db.sqlite3' for simplicity
    }
}




DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
WAGTAIL_I18N_ENABLED = True

LANGUAGES = [
    ('en', 'English'),
    ('ar', 'Arabic'),
    ('fr', 'French'),
    ('tr', 'Turkish'),
    ('de', 'German'),
    ('es', 'Spanish'),
    ('pl', 'Polish'),
    ('pt', 'Portuguese'),
    ('hu', 'Hungarian'),
    ('ru', 'Russian'),
]

WAGTAIL_CONTENT_LANGUAGES = LANGUAGES
WAGTAILLOCALIZE_SYNC_TREE = True



LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = root('static')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)



# Django compressor settings
# http://django-compressor.readthedocs.org/en/latest/settings/

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

COMPRESS_CACHEABLE_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

COMPRESS_OFFLINE = False



# Google Maps Key

GOOGLE_MAPS_KEY = ''
DYNAMIC_MAP_URL = ''
STATIC_MAP_URL = ''

# Wagtail settings

LOGIN_URL = 'wagtailadmin_login'
LOGIN_REDIRECT_URL = 'wagtailadmin_home'

WAGTAIL_SITE_NAME = "dentidelil"

# Good for sites having less than a million pages.
# Use Elasticsearch as the search backend for extra performance search results
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
    },
}

# Celery settings
# When you have multiple sites using the same Redis server,
# specify a different Redis DB. e.g. redis://localhost/5

BROKER_URL = 'redis://'

CELERY_SEND_TASK_ERROR_EMAILS = True
CELERYD_LOG_COLOR = False


AZURE_ACCOUNT_NAME = 'denti'

AZURE_ACCOUNT_KEY = '+dgCLIxs2APYUCNRPqv07I++RvZH2v7WSyZGKZFj397wGcD29HflL1gKuCdjqnRQqHW4PGqGR6pA+AStd2PAfQ=='

AZURE_CONTAINER = 'media'

DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'

# URL for accessing media files via Azure Blob Storage
MEDIA_URL = f'https://denti.blob.core.windows.net/media/'
MEDIA_ROOT = ''


WAGTAILLOCALIZE_MACHINE_TRANSLATOR = {
    "CLASS": "translations.azure.AzureTranslator",
    "OPTIONS": {
        'subscription_key': '106c8f6b95a4460fae580599a6c74348',  # Replace with your Azure key
        'region': 'uaenorth',
    }
}

# Azure settings (adjust as needed)
class AzureMediaStorage(AzureStorage):
    account_name = 'denti2'  # Replace with your actual account name
    account_key = 'KB/figw+2rVzw5WKedTHyoDfQd7X3jsmC0n2L15ALbeImxjK4sWpxYaeq2ICvVk8g9enQ9Dnx682+AStJPnL9Q=='  # Replace with your actual account key
    azure_container = 'dentistorage'  # Replace with your actual container name
    expiration_secs = None

