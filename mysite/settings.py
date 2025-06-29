"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno con prioridad al archivo .env
env_path = BASE_DIR / '.env'
load_dotenv(env_path, override=True)  # override=True da prioridad al archivo

# Detectar si estamos en Vercel o entorno serverless
IS_VERCEL = (
    os.getenv('VERCEL') == '1' or 
    os.getenv('VERCEL_ENV') is not None or
    os.getenv('VERCEL_URL') is not None
)

# Detectar si estamos en Railway
IS_RAILWAY = os.getenv('RAILWAY_ENVIRONMENT') is not None

# Detectar si estamos en Render
IS_RENDER = os.getenv('RENDER') == 'True'

# Detectar si estamos en cualquier entorno de producción
IS_PRODUCTION = IS_VERCEL or IS_RAILWAY or IS_RENDER or os.getenv('PRODUCTION') == 'True'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key-only-for-development')

# SECURITY WARNING: don't run with debug turned on in production!
# Para desarrollo local, permitir DEBUG=True por defecto si no está en producción
DEBUG = os.getenv('DEBUG', 'True' if not IS_PRODUCTION else 'False').lower() == 'true'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.vercel.app', '.railway.app', '.onrender.com', 'apihack3r-production.up.railway.app']

# CSRF settings para Railway
CSRF_TRUSTED_ORIGINS = [
    'https://apihack3r-production.up.railway.app',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://*.railway.app',
    'https://*.vercel.app',
    'https://*.onrender.com',
]

# Session settings
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Requerido por allauth
    'rest_framework',  # Esto es para agregar REST Framework
    'rest_framework.authtoken',  # Es para agregar el token de autenticación
    'dj_rest_auth',  # Usando dj-rest-auth en lugar de rest_auth
    'allauth',  # Django allauth
    'allauth.account',  # Para cuentas de usuario
    'allauth.socialaccount',  # Para cuentas sociales
    'dj_rest_auth.registration',  # Para registro de usuarios
    'corsheaders',  # Añadir corsheaders
    'django_filters',  # Añadir django-filters para filtrado avanzado
    'blog',
    'django_celery_beat',  # Añadir django-celery-beat
    'drf_yasg',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Añadir CorsMiddleware al principio
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Añadir whitenoise aquí
    'blog.middleware.SecurityHeadersMiddleware',  # Headers de seguridad personalizados
    'blog.middleware.RequestLoggingMiddleware',  # Logging de solicitudes
    'blog.middleware.APIUsageMiddleware',  # Monitoreo de uso de API
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Middleware de allauth
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'mysite.wsgi.application'

# Django REST framework settings
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.openapi.AutoSchema",
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': tmpPostgres.path[1:],  # Eliminar el primer carácter '/' del path
        'USER': tmpPostgres.username,
        'PASSWORD': tmpPostgres.password,
        'HOST': tmpPostgres.hostname,
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Cambiar a 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://apihack3r-production.up.railway.app",
    "https://hackrlabs.vercel.app",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False

# Para el Django Admin, permitir todos los headers necesarios
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Configuración de Redis y Celery
if IS_VERCEL:
    # En Vercel, construir URL de Redis desde variables de Upstash
    upstash_host = os.getenv('UPSTASH_REDIS_HOST')
    upstash_port = os.getenv('UPSTASH_REDIS_PORT', '6379')
    upstash_token = os.getenv('UPSTASH_REDIS_REST_TOKEN')
    upstash_ssl = os.getenv('UPSTASH_REDIS_SSL', 'False').lower() == 'true'
    
    # También verificar si hay URL directa
    redis_url = os.getenv('REDIS_URL')
    
    if upstash_host and upstash_token:
        # Construir URL para Upstash Redis
        protocol = 'rediss' if upstash_ssl else 'redis'
        redis_url = f"{protocol}://default:{upstash_token}@{upstash_host}:{upstash_port}"
        
        CELERY_BROKER_URL = redis_url
        CELERY_RESULT_BACKEND = redis_url
          # Configuración específica para Upstash Redis
        CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
        CELERY_BROKER_TRANSPORT_OPTIONS = {
            'global_keyprefix': 'celery_',
            'retry_policy': {
                'timeout': 5.0
            }        }
        
    elif redis_url:
        # Si hay Redis URL directa disponible
        CELERY_BROKER_URL = redis_url
        CELERY_RESULT_BACKEND = redis_url
    else:
        # Sin Redis en Vercel - ejecutar tareas síncronamente
        CELERY_TASK_ALWAYS_EAGER = True
        CELERY_TASK_EAGER_PROPAGATES = True
elif IS_RAILWAY or IS_RENDER:
    # En Railway/Render - usar Redis URL directa
    redis_url = os.getenv('REDIS_URL')
    if redis_url:
        CELERY_BROKER_URL = redis_url
        CELERY_RESULT_BACKEND = redis_url
        CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
    else:
        # Fallback a ejecución síncrona si no hay Redis
        CELERY_TASK_ALWAYS_EAGER = True
        CELERY_TASK_EAGER_PROPAGATES = True
else:
    # Desarrollo local con Redis local
    CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Configuración de Celery Beat (solo en desarrollo local)
if not IS_VERCEL and not IS_RAILWAY and not IS_RENDER:
    CELERY_BEAT_SCHEDULE = {
        # Tarea para eliminar ofertas expiradas cada día a las 2 AM
        'eliminar_ofertas_expiradas': {
            'task': 'blog.tasks.eliminar_ofertas_expiradas',
            'schedule': 86400.0,  # Ejecutar cada 24 horas
        },
        # Generar reporte de estadísticas cada semana
        'generar_reporte_estadisticas': {
            'task': 'blog.tasks.generar_reporte_estadisticas',
            'schedule': 604800.0,  # Ejecutar cada 7 días
        },
        # Limpiar logs antiguos cada mes
        'limpiar_logs_antiguos': {
            'task': 'blog.tasks.limpiar_logs_antiguos',
            'schedule': 2592000.0,  # Ejecutar cada 30 días
            'kwargs': {'dias': 30}
        },
    }
else:
    # En Vercel/Railway/Render, usar configuración optimizada para producción
    CELERY_BEAT_SCHEDULE = {
        # Solo tareas esenciales en producción
        'eliminar_ofertas_expiradas': {
            'task': 'blog.tasks.eliminar_ofertas_expiradas',
            'schedule': 86400.0,  # Ejecutar cada 24 horas
        },
    }

# Cloud storage settings
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

# Logging configuration
if IS_PRODUCTION:
    # Configuración para entornos de producción (solo consola)
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
            'json': {
                'format': '{"level": "%(levelname)s", "time": "%(asctime)s", "module": "%(module)s", "message": "%(message)s"}',
                'style': '%',
            },
        },        'handlers': {
            'null': {
                'class': 'logging.NullHandler',
            },
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
            'console_json': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'json',
            },
        },
        'root': {
            'handlers': ['console'],
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'blog': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'api_usage': {
                'handlers': ['console_json'],
                'level': 'INFO',
                'propagate': False,
            },
            'celery': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }
else:
    # Configuración para desarrollo local (con archivos)
    # Crear directorio de logs si no existe
    logs_dir = os.path.join(BASE_DIR, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
            'json': {
                'format': '{"level": "%(levelname)s", "time": "%(asctime)s", "module": "%(module)s", "message": "%(message)s"}',
                'style': '%',
            },
        },        'handlers': {
            'null': {
                'class': 'logging.NullHandler',
            },
            'file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
                'maxBytes': 1024*1024*10,  # 10 MB
                'backupCount': 5,
                'formatter': 'verbose',
            },
            'api_usage_file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(BASE_DIR, 'logs', 'api_usage.log'),
                'maxBytes': 1024*1024*5,  # 5 MB
                'backupCount': 3,
                'formatter': 'json',
            },
            'error_file': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(BASE_DIR, 'logs', 'errors.log'),
                'maxBytes': 1024*1024*10,  # 10 MB
                'backupCount': 5,
                'formatter': 'verbose',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
        },
        'root': {
            'handlers': ['console'],
        },
        'loggers': {
            'django': {
                'handlers': ['file', 'console', 'error_file'],
                'level': 'INFO',
                'propagate': False,
            },
            'blog': {
                'handlers': ['file', 'console', 'error_file'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'api_usage': {
                'handlers': ['api_usage_file'],
                'level': 'INFO',
                'propagate': False,
            },
            'celery': {
                'handlers': ['file', 'console'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }

# REST AUTH Settings
REST_AUTH = {
    'USE_JWT': False,
    'SESSION_LOGIN': True,
    'LOGIN_SERIALIZER': 'dj_rest_auth.serializers.LoginSerializer',
    'TOKEN_SERIALIZER': 'dj_rest_auth.serializers.TokenSerializer',
    'USER_DETAILS_SERIALIZER': 'dj_rest_auth.serializers.UserDetailsSerializer',
    'PASSWORD_RESET_SERIALIZER': 'dj_rest_auth.serializers.PasswordResetSerializer',
    'PASSWORD_RESET_CONFIRM_SERIALIZER': 'dj_rest_auth.serializers.PasswordResetConfirmSerializer',
    'PASSWORD_CHANGE_SERIALIZER': 'dj_rest_auth.serializers.PasswordChangeSerializer',
}

# Login redirect settings
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/api/docs/'
LOGOUT_REDIRECT_URL = '/api/docs/'

# Site ID for django-allauth
SITE_ID = 1

# Account settings (nueva configuración para evitar warnings)
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGIN_METHODS = ['username']  # Reemplaza ACCOUNT_AUTHENTICATION_METHOD
ACCOUNT_SIGNUP_FIELDS = ['username*', 'password1*', 'password2*']  # Reemplaza ACCOUNT_EMAIL_REQUIRED