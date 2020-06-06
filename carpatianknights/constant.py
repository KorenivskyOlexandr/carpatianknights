import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bd5fk4luo2v+ao3*$-w=@15f9(x)4-4q(odl@%t(lp9ibg-&_^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'myproject',
#         'USER': 'admin',
#         'PASSWORD': 's5a5s5h5a5',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }

EMAIL_HOST_USER = 'carpatianknights@gmail.com'
EMAIL_HOST_PASSWORD = 'carpatian2019'


COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
