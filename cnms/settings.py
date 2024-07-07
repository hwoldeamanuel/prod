"""
Django settings for cnms project.

Generated by 'django-admin startproject' using Django 4.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/

"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.



BASE_DIR = Path(__file__).resolve().parent.parent




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = "django-insecure-&3ep*035k@21#4lh)ex_l&=797@9u6af_3!*%$mx_8^p8=(d*^')"
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS =  ['127.0.0.1', 'https://conceptnote.azurewebsites.net']




# Application definition

INSTALLED_APPS = [
    'home',
    'program',
    'app_admin',
    'portfolio',
    'user',
    'report',
    'conceptnote',
    
    'django_htmx',
    
    'django_extensions',
    'crispy_forms',
    'django_select2',
    'django.contrib.humanize',
    
    
    'easyaudit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'crispy_bootstrap4',
    'widget_tweaks',
 
  
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
   
    
]



ROOT_URLCONF = 'cnms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cnms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

import dj_database_url
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'paqcnms',
            'USER': 'paq_admin',
            'PASSWORD': 'Letmin@2024',
            'HOST': 'conceptnote.postgres.database.azure.com',
            'PORT': '5432',
            
        }
    }



#database_url = os.environ.get("DATABASE_URL")
#DATABASES = {
 #   "default" : dj_database_url.parse(database_url)
   
#}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
#STATIC_URL = '/static/'
#Location of static files
#STATICFILES_DIRS = [
#   os.path.join(BASE_DIR, 'static'), ]
# This production code might break development mode, so we check whether we're in DEBUG mode
#if not DEBUG:
    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
#   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
 #  STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    #STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



LOGIN_REDIRECT_URL = 'user'
LOGOUT_REDIRECT_URL = 'login'




LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Addis_Ababa'

USE_I18N = True

USE_TZ = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = "CNMS App"
EMAIL_HOST_USER = "habtamuwh@gmail.com"
EMAIL_HOST_PASSWORD = "rnqc nqhx ijse kebm"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# Update Staticfiles directory
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Add azure web app as trusted CRSF
CRSF_TRUSTED_ORIGINS = ["conceptnote.azurewebsites.net"]



SELECT2_JS = "https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.12/js/select2.min.js"
SELECT2_CSS = "https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.12/css/select2.min.css"
SELECT2_I18N_PATH = "https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.12/js/i18n"