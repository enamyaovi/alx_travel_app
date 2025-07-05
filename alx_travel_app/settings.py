import environ
import os
from pathlib import Path

#creating an in module variable for retrieving info from .env file
env = environ.Env() #took out predefinition of DEBUG

# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# determine from .env file if in Production/ Development Stage
ENVIRONMENT = env('STAGE', cast=str, default='production')

# setting debug based on dev/prod
DEBUG = env(f'DEBUG_{ENVIRONMENT.upper()}', cast=bool, default=False)

ALLOWED_HOSTS = env.list(f'ALLOWED_HOSTS_{ENVIRONMENT.upper()}', cast=list,default=[])


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY') #uses smart casting


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #third party packages
    'drf_yasg',
    'rest_framework',
    'corsheaders',

    #apps
    'listings.app.ListingsConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'alx_travel_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'alx_travel_app.wsgi.application'


# Database
# resolves the database based on whether in production or development environment as set in the .env file. Otherwise default to using the mysqlite db
DATABASES = {
    'default': env.db(f'DATABASE_{ENVIRONMENT.upper()}', default='sqlite:////mysqlite.sqlite3'),
}


# Password Settings

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


PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'



# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#CORS ALLOWED ORIGINS
CORS_ALLOWED_ORIGINS = env.list(f'CORS_{ENVIRONMENT.upper()}')

#REST FRAMEWORK SETTINGS
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'EXCEPTION_HANDLER': 'utils.exceptionhandler.customexceptionhandler',
}

#swagger settings
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        # Basic Authentication
        'Basic': {
            'type': 'basic',  
        },
        # Bearer Token Authentication (JWT)
        'Bearer': {
            'type': 'apiKey',  
            'name': 'Authorization',  
            'in': 'header',  
            'description': 'JWT token for user authentication',  
        },
        # Token Authentication (DRF token authentication)
        'Token': {
            'type': 'apiKey', 
            'name': 'Authorization', 
            'in': 'header',  
            'description': 'Token for user authentication',  
        }
    },    
}

#extra security configurations for production mode only
if ENVIRONMENT == 'production':
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_BROWSER_XSS_FILTER = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True  
    SECURE_HSTS_PRELOAD = True  
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') 