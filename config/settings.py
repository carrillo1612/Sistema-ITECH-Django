from pathlib import Path
import os  # <--- AGREGA ESTA LÍNEA AQUÍ ARRIBA
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-4=)vd$6e=6yvw$a)y==wk2592xfz-ngz$y02ab3nvf%fd-isua')

# SECURITY WARNING: don't run with debug turned on in production!
# La variable de entorno de Render será 'False' en producción
DEBUG = os.environ.get('DEBUG') == 'True'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.68.110', '192.168.1.112', '192.168.1.168']

# Añade el host de Render para que pueda acceder
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
# Application definition

INSTALLED_APPS = [
    'servicios',  # <--- AÑADE ESTA LÍNEA
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# settings.py

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'), # Lee la URL de Render
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
LANGUAGE_CODE = 'es-mx'  # <--- Cambiado a Español México

TIME_ZONE = 'America/Mexico_City' # <--- Cambiado a hora del centro de México

USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
# Asegúrate de que esta línea use os.path.join
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# Define la carpeta donde Django recolectará todos los archivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # <-- ¡AÑADE ESTA LÍNEA!
# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login/'
# --- ESTA ES LA LÍNEA CLAVE ---
LOGIN_REDIRECT_URL = 'lista_clientes' # Asegúrate de que sea 'lista_clientes'

LOGOUT_REDIRECT_URL = 'login'

# config/settings.py

AUTH_USER_MODEL = 'servicios.Usuarios'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'servicios.backends.EmailBackend',
]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TELEGRAM_BOT_TOKEN = '8205329300:AAHPQG-YuMIcrwM3a2bNgWUa2SdpLdFlQIw' 
TELEGRAM_CHAT_ID = '-5045908595'