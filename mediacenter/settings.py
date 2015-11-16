import os
from credentials import *

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SECRET_KEY = 'km$_)t_hn&a0eb-6cgymcwr9-f8#4p2hgxjp))eu_&wp8cxg*@'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ["127.0.0.1"]


AUTH_USER_MODEL = "backend.User"
SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

DEFAULT_FROM_EMAIL = "danjamesbond@gmail.com"
EMAIL_FROM = "Daniel Bond <danjamesbond@gmail.com>"
ADMINS = (("Daniel Bond", "danjamesbond@gmail.com"),)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True


SOCIAL_AUTH_FORCE_POST_DISCONNECT = True
SOCIAL_AUTH_URLOPEN_TIMEOUT = 30
SOCIAL_AUTH_SESSION_EXPIRATION = False

SOCIAL_AUTH_REDIRECT_IS_HTTPS = False

SOCIAL_AUTH_RAISE_EXCEPTIONS = DEBUG
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = []
SOCIAL_AUTH_GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True
SOCIAL_AUTH_REVOKE_TOKENS_ON_DISCONNECT = True
SOCIAL_AUTH_BACKEND_ERROR_URL = '/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/index/'

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social.pipeline.social_auth.social_uid',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social.pipeline.social_auth.social_user',

    # create a User record if it doesn't exist already, and is in ALLOWED_DOMAINS
    'frontend.pipeline.create_if_nonexistent',

    # Associates the current social details with an existing user record
    'frontend.pipeline.associate_by_email',

    # if user isn't allowed to login, redirect to homepage
    'frontend.pipeline.login_check',

    # Create the record that associated the social account with this user.
    'social.pipeline.social_auth.associate_user',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social.pipeline.social_auth.load_extra_data',

    # Update the user record with any changed info from the auth service.
    'social.pipeline.user.user_details'
)

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GooglePlusAuth',
    'django.contrib.auth.backends.ModelBackend',
)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

########### END AUTH ###########



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
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
)

ROOT_URLCONF = 'mediacenter.urls'

WSGI_APPLICATION = 'mediacenter.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/srv/db/mediacenter.db'
        # 'NAME': 'mediacenter',
        # 'USER': 'mediacenter',
        # 'PASSWORD': DB_PASS,
        # 'HOST': "173.194.248.178",
        # 'PORT': 3306,
        # 'OPTIONS': {
        #     'init_command': 'SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED',
        #     'ssl': {
        #         'ca': '/etc/ssl/sql/server-ca.pem',
        #         'cert': '/etc/ssl/sql/client-cert.pem',
        #         'key': '/etc/ssl/sql/client-key.pem'
        #     }
        # }
    }
}


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
