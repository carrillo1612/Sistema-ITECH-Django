from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('servicios.urls')), # <--- AÑADE ESTA LÍNEA
]

if settings.DEBUG:
    # Este bloque solo funciona si settings está importado
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)