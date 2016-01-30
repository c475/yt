import os
from credentials import *

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'km$_)t_hn&a0eb-6cgymcwr9-f8#4p2hgxjp))eu_&wp8cxg*@'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ["127.0.0.1"]

AUTH_USER_MODEL = "backend.User"
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/rooms/"
LOGOUT_REDIRECT_URL = "/login/"

DEFAULT_FROM_EMAIL = "danjamesbond@gmail.com"
EMAIL_FROM = "Daniel Bond <danjamesbond@gmail.com>"
ADMINS = (("Daniel Bond", "danjamesbond@gmail.com"),)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True


AUTHENTICATION_BACKENDS = (
    'social.backends.google.GooglePlusAuth',
    'django.contrib.auth.backends.ModelBackend',
)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptPasswordHasher',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'frontend',
    'backend',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mediacenter.middleware.VariousHeaders'
)

ROOT_URLCONF = 'mediacenter.urls'

WSGI_APPLICATION = 'mediacenter.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/srv/db/mediacenter.db'
    }
}

SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_HOST = 'localhost'
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 0
SESSION_REDIS_PREFIX = 'session'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "frontend/templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.messages.context_processors.messages",
    "django.contrib.auth.context_processors.auth",
)

TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "frontend", "assets"),
)

STATIC_ROOT = os.path.join(BASE_DIR, "frontend", "static")

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)
