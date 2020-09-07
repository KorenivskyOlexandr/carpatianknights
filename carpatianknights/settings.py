"""
Django settings for carpatianknights project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import carpatianknights.constant as constant

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = constant.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = constant.DEBUG

ALLOWED_HOSTS = constant.ALLOWED_HOSTS

# Application definition

INSTALLED_APPS = [
    'carpatianknights.account',

    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'carpatianknights.news',
    'carpatianknights.front_end',
    'carpatianknights.route',

    'django_filters',
    'taggit',
    # 'sass_processor',
    # 'compressor',
    # 'compressor_toolkit',
    # 'svg',
    # 'webpack_loader',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'carpatianknights.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'carpatianknights/front_end/templates')],
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

WSGI_APPLICATION = 'carpatianknights.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = constant.DATABASES

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
# STATIC_ROOT = os.path.join(BASE_DIR, 'carpatianknights/front_end/static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'sass_processor.finders.CssFinder',
    # 'compressor.finders.CompressorFinder',
]

# SASS_PROCESSOR_ROOT = STATIC_ROOT

# SASS_PROCESSOR_INCLUDE_DIRS = [
#     os.path.join(BASE_DIR, 'extra-styles/scss'),
#     os.path.join(BASE_DIR, 'node_modules'),
# ]

# SASS_PROCESSOR_INCLUDE_FILE_PATTERN = r'^.+\.scss$'
# SASS_PRECISION = 8

# COMPRESS_PRECOMPILERS = (
#     ('text/x-scss', 'django_libsass.SassCompiler'),
# )

LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = constant.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = constant.EMAIL_HOST_PASSWORD

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'carpatianknights.account.authentication.EmailAuthBackend',
]

# STATICFILES_FINDERS += (
#     'compressor.finders.CompressorFinder',
# )
#
# COMPRESS_CSS_FILTERS = [
#     'compressor.filters.css_default.CssAbsoluteFilter',
#     'compressor.filters.cssmin.CSSMinFilter',
#     'compressor.filters.template.TemplateFilter'
# ]
# COMPRESS_JS_FILTERS = [
#     'compressor.filters.jsmin.JSMinFilter',
# ]
# COMPRESS_PRECOMPILERS = (
#     ('module', 'compressor_toolkit.precompilers.ES6Compiler'),
#     ('css', 'compressor_toolkit.precompilers.SCSSCompiler'),
#     ('text/x-scss', 'django_libsass.SassCompiler'),
# )

# COMPRESS_ENABLED = constant.COMPRESS_ENABLED
# COMPRESS_OFFLINE = constant.COMPRESS_OFFLINE

SERVER = constant.SERVER

# Webpack settings

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'dist'),
)

# WEBPACK_LOADER = {
#     'DEFAULT': {
#         'CACHE': not DEBUG,
#         'BUNDLE_DIR_NAME': 'webpack_bundles/', # must end with slash
#         'STATS_FILE': os.path.join(BASE_DIR, 'src/webpack_bundles/webpack-stats.json'),
#         'POLL_INTERVAL': 0.1,
#         'TIMEOUT': None,
#         'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
#         'LOADER_CLASS': 'webpack_loader.loader.WebpackLoader',
#     }
# }
