# servicios/urls.py
from django.views.generic.base import RedirectView # <-- 1. IMPORTAR REDIRECTVIEW
from django.urls import path
from . import views

urlpatterns = [
    # --- NUEVA RUTA: Redirige la raíz (/) al login (/login/) ---
    # Usamos permanent=False para que sea una redirección 302 (temporal)
    path('', RedirectView.as_view(pattern_name='login', permanent=False), name='root-redirect'),

    # (Clientes)
    path('clientes/', views.vista_clientes, name='lista_clientes'),
    path('clientes/editar/<int:id>/', views.vista_clientes, name='editar_cliente'),
    path('clientes/eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),

    # (Ordenes)
    path('ordenes/', views.lista_ordenes, name='lista_ordenes'),
    path('ordenes/editar/<int:id>/', views.editar_orden, name='editar_orden'),
    path('ordenes/eliminar/<int:id>/', views.eliminar_orden, name='eliminar_orden'),

    # (Usuarios)
    path('usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    path('usuarios/editar/<int:id>/', views.gestion_usuarios, name='editar_usuario'),
    path('usuarios/eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),

    # (Calendario)
    path('calendario/', views.vista_calendario, name='vista_calendario'),
    path('calendario/data/', views.calendario_data, name='calendario_data'),

    # ESTA ES LA NUEVA RUTA para la página de "Generar Reporte"
    path('reportes/pendientes/', views.lista_reportes_pendientes_view, name='lista_reportes_pendientes'),
    path('ordenes/pdf_abrir/<int:orden_id>/', views.generar_y_abrir_pdf, name='generar_y_abrir_pdf'),

    path('registro_temp/<int:orden_id>/', views.generar_registro, name='registro_temp'),

    path('registro-tecnico/guardar/', views.guardar_registro_tecnico, name='guardar_registro_tecnico'),
    # Usará el ID de la orden para encontrar y mostrar el reporte
    path('reporte/ver/<int:orden_id>/', views.ver_reporte_view, name='ver_reporte'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    # --- NUEVA RUTA DE API PARA DETALLES DE CLIENTE ---
    path('api/get_client_details/<int:cliente_id>/', views.get_client_details, name='get_client_details'),
]
