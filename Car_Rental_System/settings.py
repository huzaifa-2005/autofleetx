from pathlib import Path
import os
from decouple import config, Csv
import dj_database_url
from django.core.management.utils import get_random_secret_key
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY', default=get_random_secret_key())
try:
    ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
except Exception:
    # Fallback for development
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

if not ALLOWED_HOSTS:
    raise ImproperlyConfigured("ALLOWED_HOSTS must be set in environment variables for production.")
DEBUG = config("DEBUG", default=False, cast=bool)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main_app.apps.MainAppConfig',  
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'rest_framework',
    'api',
]
AUTH_USER_MODEL = 'main_app.CustomUser'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  
    'django.contrib.sessions.middleware.SessionMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'Car_Rental_System.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Required by allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'Car_Rental_System.wsgi.application'
DATABASE_URL = config("DATABASE_URL", default="")
if DATABASE_URL:
    try:
        DATABASES = {
            'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
        }
        # Adding ENGINE explicitly for better compatibility
        DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'
    except ValueError as e:
        raise ImproperlyConfigured(f"Invalid DATABASE_URL: {e}")
else:
        # Preferring failing loudly if DATABASE_URL is missing in production and dev as well.
        raise ImproperlyConfigured("DATABASE_URL is not set in production!")    

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'
#keeping this (below) on will let add translations later (if needed).
USE_I18N = True
USE_TZ = True
# Static files configuration 
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] #where to look for static files during development
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# user uploads configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
#----LOGIN & LOGOUT URL SETTINGS
LOGIN_REDIRECT_URL = '/' # Where to send the user after successful login (Google/local) both.
LOGOUT_REDIRECT_URL = '/login/' # Where to send the user after logout.
LOGIN_URL = '/login/' # redirecting user here when not logged in and tries to access a protected view

#----ACCOUNT BEHAVIOR (LOCAL + SOCIAL)
ACCOUNT_EMAIL_VERIFICATION = 'none'  # No email verification required (login/signup will not be blocked).
ACCOUNT_LOGOUT_ON_GET = True         # Logout occurs immediately on GET request (no confirmation screen).
# Local login config: allows login with username (could also be email if extended).
ACCOUNT_LOGIN_METHODS = {'username'}
# Fields required for signup (applies to local account creation).
ACCOUNT_SIGNUP_FIELDS = ['email', 'username*', 'password1*', 'password2*']

#----SIGNUP REDIRECT + AUTO-SIGNUP FOR GOOGLE ACCOUNTS
# Redirect after signup (applies when a NEW user logs in via Google
# and their local User instance gets created in our DB).
ACCOUNT_SIGNUP_REDIRECT_URL = '/'
SOCIALACCOUNT_AUTO_SIGNUP = True # Automatically create a user if logging in via Google for the first time.
# Custom adapter: to override AllAuth's default behavior
# (auto-linking Google account to existing local account, i.e. appling custom validation)
SOCIALACCOUNT_ADAPTER = 'main_app.adapters.MySocialAccountAdapter'

#----SOCIAL ACCOUNT PROVIDER CONFIG
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID'),
            'secret': config('GOOGLE_CLIENT_SECRET'),
            'key': ''
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'prompt': 'select_account'}
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
#----CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://autofleetx-production-c144.up.railway.app',
]
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', cast=int, default=587)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
