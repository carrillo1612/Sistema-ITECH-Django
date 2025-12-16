from pathlib import Path
import os 
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-4=)vd$6e=6yvw$a)y==wk2592xfz-ngz$y02ab3nvf%fd-isua')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == 'True'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.68.110', '192.168.1.112', '192.168.1.168']

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition
INSTALLED_APPS = [
    'servicios', 
    'storages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'), 
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'es-mx'  
TIME_ZONE = 'America/Mexico_City' 

USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = 'lista_clientes' 
LOGOUT_REDIRECT_URL = 'login'

AUTH_USER_MODEL = 'servicios.Usuarios'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'servicios.backends.EmailBackend',
]

# =========================================================================
# ⚙️ CONFIGURACIÓN DE ALMACENAMIENTO PERMANENTE (AWS S3) - MODO FIRMADO
# =========================================================================

# 1. Credenciales (Asegurarse de que estén en el panel Environment de Render)
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

# 2. Especificar la región del bucket
AWS_S3_REGION_NAME = 'us-west-2' 

# 3. Indicar a Django que use S3 para almacenar archivos subidos (MEDIA)
DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'

# 4. Configuración de Dominio y URL
# IMPORTANTE: AWS_S3_CUSTOM_DOMAIN debe ser None y MEDIA_URL NO debe definirse 
# manualmente para que django-storages genere las firmas de seguridad.
AWS_S3_CUSTOM_DOMAIN = None
# 5. Seguridad y Firmas (Esto genera el token ?X-Amz-Algorithm... en las URLs)
AWS_QUERYSTRING_AUTH = True  
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None # Usamos permisos privados porque la firma autoriza el acceso

# =========================================================================

TELEGRAM_BOT_TOKEN = '8205329300:AAHPQG-YuMIcrwM3a2bNgWUa2SdpLdFlQIw' 
TELEGRAM_CHAT_ID = '-5045908595'