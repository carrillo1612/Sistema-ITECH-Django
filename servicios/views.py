from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required # Se mantiene para cuando lo necesites
from .models import Clientes, OrdenesServicio, Usuarios, OrdenDetalles, RegistrosTecnicos, RegistroFotos
from .forms import ClienteForm, OrdenServicioForm, UsuarioForm
from django.contrib.auth.hashers import make_password # Necesario si lo usas en form.save
from django.http import JsonResponse
import json
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth import authenticate, login, logout 
from django.core.files.base import ContentFile  # <--- ¡ESTA ES LA QUE TE FALTA!
import os
from django.conf import settings
import base64  # <--- ¡AGREGA ESTO!
from django.utils import timezone
import qrcode
from io import BytesIO
from django.db.models import Q  # <--- AGREGA ESTO
from datetime import datetime, time
from django.utils.dateparse import parse_date
import requests
from django.conf import settings
from django.urls import reverse



# Importa tus modelos
from .models import (
    Usuarios, 
    Clientes, 
    OrdenesServicio, 
    OrdenDetalles, 
    RegistrosTecnicos, 
    RegistroFotos
)

# ----------------------------------------------------------------------
# FUNCIONES DE AYUDA (DEFINIDAS AL INICIO PARA EVITAR NameError)
# ----------------------------------------------------------------------

def _check_admin_access(request):
    """
    Verifica si el usuario es Administrador o Soporte.
    Si es Técnico, redirige al calendario.
    """
    # Compara con el valor 'Técnico' (con tilde)
    if request.user.Rol == 'Técnico':
        messages.error(request, 'Acceso denegado. No tienes permisos para esta sección.')
        return redirect('vista_calendario')
    return None # Si es Admin o Soporte, permite continuar

# ----------------------------------------------------------------------
# VISTAS CRUD (DECORADORES COMENTADOS PARA PERMITIR ACCESO)
# ----------------------------------------------------------------------

@login_required 
def vista_clientes(request, id=None):
    # 🛑 RESTRICCIÓN: Solo Administrador
    # (Asumimos que check_admin_only está definido y funciona correctamente)
    response = check_admin_only(request)
    if response: return response
    
    # --- 1. Lógica de Edición/Creación (POST) ---
    if id:
        cliente_instancia = get_object_or_404(Clientes, pk=id)
    else:
        cliente_instancia = None

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente_instancia)
        
        if form.is_valid():
            form.save()
            accion = "actualizado" if cliente_instancia else "creado"
            messages.success(request, f"Cliente '{form.cleaned_data['NombreComercial']}' {accion} exitosamente.")
            return redirect('lista_clientes')
        
    else: # Método GET
        form = ClienteForm(instance=cliente_instancia)

    # --- 2. 🚀 LÓGICA DE LISTADO Y BÚSQUEDA (GET) 🚀 ---
    
    # QuerySet base: Obtener todos los clientes
    todos_los_clientes = Clientes.objects.all().order_by('ClienteID') # Ordenar por ID o Nombre
    
    # Leer el parámetro de búsqueda 'q' de la URL
    query = request.GET.get('q')

    # Aplicar filtro si se proporciona un término de búsqueda
    if query:
        # Usamos Q objects para buscar por Nombre Comercial, Ciudad, Correo, Teléfono
        todos_los_clientes = todos_los_clientes.filter(
            Q(NombreComercial__icontains=query) |
            Q(Ciudad__icontains=query) |
            Q(Correo__icontains=query) |
            Q(Telefono__icontains=query)
        ).distinct()
    
    # --- FIN LÓGICA DE BÚSQUEDA ---
    
    # 3. Pasar la lista filtrada al contexto
    contexto = {
        'lista_de_clientes': todos_los_clientes, # Pasamos la QuerySet filtrada
        'form': form,
        'cliente_a_editar': cliente_instancia
    }
    return render(request, 'servicios/clientes.html', contexto)

@login_required # <-- COMENTADO TEMPORALMENTE
def eliminar_cliente(request, id):
    # 🛑 RESTRICCIÓN: Solo Administrador
    response = check_admin_only(request)
    if response: return response
    if request.method == 'POST':
        try:
            cliente = get_object_or_404(Clientes, pk=id)
            nombre_cliente = cliente.NombreComercial
            cliente.delete()
            messages.success(request, f"Cliente '{nombre_cliente}' eliminado exitosamente.")
        except Exception as e:
            messages.error(request, f"Error al eliminar cliente: {e}")
    return redirect('lista_clientes')


@login_required
def lista_ordenes(request):
    # 🛑 RESTRICCIÓN DE LECTURA (GET): Permitir Administrador y Técnico
    if request.user.Rol not in ['Administrador', 'Técnico']:
        messages.error(request, 'Acceso denegado. Solo personal operativo puede ver las órdenes.')
        return redirect('vista_calendario') 

    # 1. LÓGICA DE GUARDADO (POST) - RESTRINGIDA A ADMINISTRADOR
    if request.method == 'POST':
        # 🛑 Bloquear la creación de órdenes si NO es Administrador
        if request.user.Rol != 'Administrador':
            messages.error(request, 'Solo Administradores pueden crear órdenes de servicio.')
            return redirect('lista_ordenes') 
        
        form = OrdenServicioForm(request.POST)
    # 1. LÓGICA DE GUARDADO (POST)
    if request.method == 'POST':
        form = OrdenServicioForm(request.POST)
        
        # Obtener listas de productos del HTML
        detalles_cantidades = request.POST.getlist('detalle_cantidad[]')
        detalles_productos = request.POST.getlist('detalle_producto[]')
        detalles_infos = request.POST.getlist('detalle_info[]')

        if form.is_valid():
            try:
                with transaction.atomic():
                    # Guardar Orden Principal
                    nueva_orden = form.save(commit=False)
                    nueva_orden.Estado = 'Pendiente'
                    nueva_orden.save()

                    # Guardar Detalles (Productos)
                    for i in range(len(detalles_productos)):
                        cantidad = detalles_cantidades[i]
                        producto = detalles_productos[i]
                        info = detalles_infos[i]

                        if producto: # Solo si hay nombre de producto
                            OrdenDetalles.objects.create(
                                Orden=nueva_orden,
                                Cantidad=int(cantidad) if cantidad and cantidad.isdigit() else 1,
                                Producto=producto,
                                InformacionAdicional=info
                            )

                # 🚀 LLAMADA CLAVE PARA LA NOTIFICACIÓN (AQUÍ DEBE IR) 🚀
                    # ----------------------------------------------------
                    enviar_notificacion_telegram(nueva_orden)
                    # ----------------------------------------------------
                
                messages.success(request, f"Orden #{nueva_orden.OrdenID} creada exitosamente.")
                return redirect('lista_ordenes')
            

            except Exception as e:
                messages.error(request, f"Error al guardar: {e}")
        else:
            # Debug de errores en consola
            print("--- ERRORES DEL FORMULARIO ---")
            print(form.errors)
            print("-------------------------------")
            messages.error(request, 'Error al guardar. Revisa los campos obligatorios.')

    # 2. LÓGICA DE FILTROS Y LISTADO (GET)
    
    # QuerySet base: Traer todas las órdenes ordenadas por ID descendente
    ordenes = OrdenesServicio.objects.select_related('ClienteEmpresa', 'PersonalAsignado').all().order_by('-OrdenID')

    # ✅ NUEVO: Lógica de la Barra de Búsqueda
    busqueda = request.GET.get('q')
    if busqueda:
        ordenes = ordenes.filter(
            Q(ClienteEmpresa__NombreComercial__icontains=busqueda) | # Busca por Cliente
            Q(OrdenID__icontains=busqueda) |                         # Busca por Folio
            Q(Servicio__icontains=busqueda) |                        # Busca por Servicio
            Q(PersonalAsignado__Nombre__icontains=busqueda)          # Busca por Técnico
        )

    # Recuperar parámetros del filtro desde la URL
    fecha_inicio = request.GET.get('date_start')
    fecha_fin = request.GET.get('date_end')
    cliente_id = request.GET.get('cliente')
    personal_id = request.GET.get('personal')
    servicio_txt = request.GET.get('servicio')
    estado_txt = request.GET.get('estado')
    busqueda_general = request.GET.get('q') # Si usas la barra de búsqueda texto

    # ... (tu código anterior de búsqueda 'q') ...

    # --- LÓGICA DE FECHAS ROBUSTA (Zona Horaria Correcta) ---
    
    if fecha_inicio:
        # 1. Convertimos texto a fecha
        f_ini = parse_date(fecha_inicio)
        if f_ini:
            # 2. Creamos la fecha con hora 00:00:00 y le ponemos la zona horaria activa
            inicio_dia = timezone.make_aware(datetime.combine(f_ini, time.min))
            # 3. Filtramos: Mayor o igual al primer segundo del día
            ordenes = ordenes.filter(Programada__gte=inicio_dia)
    
    if fecha_fin:
        f_fin = parse_date(fecha_fin)
        if f_fin:
            # 2. Creamos la fecha con hora 23:59:59.999
            fin_dia = timezone.make_aware(datetime.combine(f_fin, time.max))
            # 3. Filtramos: Menor o igual al último segundo del día
            ordenes = ordenes.filter(Programada__lte=fin_dia)

    if cliente_id and cliente_id != 'Todos':
        ordenes = ordenes.filter(ClienteEmpresa_id=cliente_id)

    if personal_id and personal_id != 'Todos':
        ordenes = ordenes.filter(PersonalAsignado_id=personal_id)

    if servicio_txt and servicio_txt != 'Todos':
        ordenes = ordenes.filter(Servicio=servicio_txt)

    if estado_txt and estado_txt != 'Todos':
        ordenes = ordenes.filter(Estado=estado_txt)

    # Datos para llenar los selectores del filtro (Dropdowns de arriba)
    clientes_filtro = Clientes.objects.all().order_by('NombreComercial')
    tecnicos_filtro = Usuarios.objects.filter(Rol='Técnico').order_by('Nombre')

    # 3. PREPARAR CONTEXTO
    # Si fue un POST fallido, 'form' ya tiene los errores. Si es GET, creamos uno vacío.
    if request.method == 'GET':
        form = OrdenServicioForm()

    context = {
        'lista_de_ordenes': ordenes,
        'form_orden': form,
        'clientes_filtro': clientes_filtro, # Para el filtro de clientes
        'tecnicos_filtro': tecnicos_filtro  # Para el filtro de técnicos
    }
    
    return render(request, 'servicios/ordenes_servicio.html', context)


@login_required
def editar_orden(request, id):
    # 🛑 RESTRICCIÓN: Solo Administrador
    response = check_admin_only(request)
    if response: return response
    # 1. Buscar la orden
    orden_editar = get_object_or_404(OrdenesServicio, pk=id)

    if request.method == 'POST':
        form = OrdenServicioForm(request.POST, instance=orden_editar)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # A. Guardar datos principales (Cliente, Fecha, Ubicación...)
                    form.save()

                    # B. ACTUALIZAR PRODUCTOS (Lógica de reemplazo)
                    # 1. Borramos todos los detalles anteriores de esta orden
                    orden_editar.ordendetalles_set.all().delete()

                    # 2. Recibimos la lista nueva desde el HTML
                    cantidades = request.POST.getlist('detalle_cantidad[]')
                    productos = request.POST.getlist('detalle_producto[]')
                    infos = request.POST.getlist('detalle_info[]')

                    # 3. Guardamos los que quedaron vivos en la lista
                    for i in range(len(productos)):
                        prod_nombre = productos[i]
                        cant = cantidades[i]
                        info = infos[i]

                        if prod_nombre: # Solo si tiene nombre
                            OrdenDetalles.objects.create(
                                Orden=orden_editar,
                                Cantidad=int(cant) if cant and cant.isdigit() else 1,
                                Producto=prod_nombre,
                                InformacionAdicional=info
                            )
                    
                    messages.success(request, f"Orden #{id} actualizada correctamente.")
                    return redirect('lista_ordenes')

            except Exception as e:
                messages.error(request, f"Error al actualizar detalles: {e}")
        else:
             messages.error(request, "Error en el formulario principal.")
    else:
        form = OrdenServicioForm(instance=orden_editar)

    # 4. Renderizar
    ordenes = OrdenesServicio.objects.select_related('ClienteEmpresa', 'PersonalAsignado').all()
    
    contexto = {
        'lista_de_ordenes': ordenes,
        'form_orden': form,
        'orden_a_editar': orden_editar,
        'abrir_modal': True
    }
    return render(request, 'servicios/ordenes_servicio.html', contexto)

@login_required # <-- COMENTADO TEMPORALMENTE
def eliminar_orden(request, id):
    if request.method == 'POST':
        try:
            orden = get_object_or_404(OrdenesServicio, pk=id)
            orden.delete()
            messages.success(request, f"Orden #{id} eliminada exitosamente.")
        except Exception as e:
             messages.error(request, f"Error al eliminar la orden #{id}: {e}")
    return redirect('lista_ordenes')


# Asegúrate de que las importaciones estén al inicio del archivo:
# from django.db.models import Q 
# from .models import Usuarios, ... (otros modelos)

@login_required 
def gestion_usuarios(request, id=None):
    # 🛑 RESTRICCIÓN: Solo Administrador
    response = check_admin_only(request)
    if response: return response
    
    # --- Lógica de Edición/Creación (POST) ---
    if id:
        usuario_instancia = get_object_or_404(Usuarios, pk=id)
        # Almacena la contraseña hasheada original para el caso de que no se cambie
        contrasena_original = usuario_instancia.password 
    else:
        usuario_instancia = None
        contrasena_original = None

    if request.method == 'POST':
        # Es necesario pasar request.POST al formulario para que procese los datos
        form = UsuarioForm(request.POST, instance=usuario_instancia)
        
        if form.is_valid():
            try:
                # Retenemos el guardado para poder modificar la contraseña
                usuario_guardado = form.save(commit=False)

                nueva_contrasena = form.cleaned_data.get('password') 
                
                # 🛠️ ZONA DE CORRECCIÓN CRÍTICA: ENCRIPTAR LA CONTRASEÑA
                if nueva_contrasena:
                    # Encripta la nueva contraseña antes de guardarla
                    usuario_guardado.set_password(nueva_contrasena) 
                
                elif usuario_instancia and contrasena_original: 
                    # Si no hay nueva contraseña (campo vacío), mantenemos la hasheada original
                    usuario_guardado.password = contrasena_original 
                
                # ⚠️ Nota: No necesitamos else if, si no es una instancia existente, 
                # el form.save() ya debería haber manejado la creación inicial de la clave
                # si fue un nuevo registro. Pero para edición, esto es esencial.

                usuario_guardado.save() # Guarda el objeto con la contraseña encriptada

                accion = "actualizado" if usuario_instancia else "creado"
                messages.success(request, f"Usuario '{usuario_guardado.Nombre}' {accion} exitosamente.")
                return redirect('gestion_usuarios')
                
            except Exception as e:
                messages.error(request, f"Error al guardar usuario: {e}")

    else: # GET para abrir modal de edición
        form = UsuarioForm(instance=usuario_instancia)
        if usuario_instancia:
            # Asegura que el campo contraseña aparezca vacío en el formulario de edición
            form.fields['password'].initial = '' 
            form.fields['password'].widget.attrs.update({'placeholder': 'Dejar en blanco para no cambiar'})
            form.fields['password'].required = False # Permite que el campo quede vacío si no se edita

    # --- 🚀 LÓGICA DE LISTADO Y BÚSQUEDA (GET) 🚀 ---
    
    # 1. QuerySet base: Obtener todos los usuarios
    usuarios = Usuarios.objects.all()

    # 2. Leer el parámetro de búsqueda 'q'
    query = request.GET.get('q')

    # 3. Aplicar filtro si se proporciona un término de búsqueda
    if query:
        # Usamos Q objects para aplicar la búsqueda OR en varios campos
        usuarios = usuarios.filter(
            Q(Nombre__icontains=query) |
            Q(Apellido__icontains=query) |
            Q(CorreoElectronico__icontains=query) |
            Q(Rol__icontains=query)
        ).distinct()
    
    # --- FIN LÓGICA DE BÚSQUEDA ---
    
    # El resto del contexto pasa la lista de usuarios filtrada
    contexto = {
        'lista_usuarios': usuarios, # Pasamos la QuerySet filtrada o sin filtrar
        'form_usuario': form,
        'usuario_a_editar': usuario_instancia,
        'query': query # Para mantener el término de búsqueda en el formulario
    }
    return render(request, 'servicios/gestion_usuarios.html', contexto)

@login_required # <-- COMENTADO TEMPORALMENTE
def eliminar_usuario(request, id):
    if request.method == 'POST':
        try:
            usuario = get_object_or_404(Usuarios, pk=id)
            nombre_usuario = f"{usuario.Nombre} {usuario.Apellido}"
            usuario.delete()
            messages.success(request, f"Usuario '{nombre_usuario}' eliminado exitosamente.")
        except Exception as e:
            messages.error(request, f"Error al eliminar usuario: {e}")
    return redirect('gestion_usuarios')


# ----------------------------------------------------------------------
# VISTAS TEMPORALES NO PROTEGIDAS (PARA DISEÑO)
# ----------------------------------------------------------------------

# 1. Vista principal (solo renderiza el template)
# En views.py
@login_required # <-- COMENTADO TEMPORALMENTE
def vista_calendario(request):
    # CORRECCIÓN: Usar el modelo Clientes (no ClienteEmpresa)
    clientes = Clientes.objects.all().order_by('NombreComercial')
    
    # CORRECCIÓN: Usar el modelo Usuarios, filtrando solo por Rol = 'Técnico'
    # Importante: ROL_TECNICO debe estar disponible si lo usas en el filtro
    ROL_TECNICO = 'Técnico' # Define esta constante si no está importada
    personal = Usuarios.objects.filter(Rol=ROL_TECNICO).order_by('Nombre')
    
    context = {
        'clientes': clientes,
        'personal': personal,
    }
    return render(request, 'servicios/calendario.html', context)

def obtener_color_por_estado(estado):
    # La función auxiliar para mapear el estado a un color
    if estado == 'Programada':
        return '#007bff'
    elif estado == 'Activa':
        return '#ffc107'
    elif estado == 'Terminada':
        return '#28a745'
    elif estado == 'Cancelada':
        return '#dc3545'
    return '#6c757d' # Color por defecto: gris

@login_required # <-- COMENTADO TEMPORALMENTE
def calendario_data(request):
    # --- 1. CAPTURAR PARÁMETROS DE FILTRO ---
    
    # Captura el valor del filtro. Si es "Todos", usaremos None o lo ignoraremos.
    cliente_filtro = request.GET.get('cliente', 'Todos')
    personal_filtro = request.GET.get('personal', 'Todos')
    estado_orden_filtro = request.GET.get('estado_orden', 'Todos')
    
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')

    # QuerySet base: Filtrar solo órdenes con fecha programada
    ordenes = OrdenesServicio.objects.select_related('ClienteEmpresa', 'PersonalAsignado').filter(Programada__isnull=False)
    
    # --- 2. APLICAR FILTROS DINÁMICOS ---
    
    # 2.1. Filtro por Rango de Fechas (Esencial de FullCalendar)
    if start_date and end_date:
        # Filtra eventos que se traslapan con el rango visible (Programada es la fecha de inicio)
        ordenes = ordenes.filter(Programada__range=[start_date, end_date])
    
    # 2.2. Filtro por Cliente (Usando ID)
    if cliente_filtro != 'Todos':
        try:
            cliente_id = int(cliente_filtro)
            # Filtra por la clave primaria del cliente al que apunta ClienteEmpresa
            ordenes = ordenes.filter(ClienteEmpresa__pk=cliente_id) 
        except ValueError:
            # Si el valor no es un ID (por si se envía otro valor), ignora o filtra por un valor imposible
            pass

    # 2.3. Filtro por Personal Asignado (Usando ID)
    if personal_filtro != 'Todos':
        try:
            personal_id = int(personal_filtro)
            # Filtra por la clave primaria del usuario al que apunta PersonalAsignado
            ordenes = ordenes.filter(PersonalAsignado__pk=personal_id) 
        except ValueError:
            # Si el valor no es un ID (por si se envía otro valor), ignora
            pass
            
    # 2.4. Filtro por Estado de Orden (Usando el valor del choice)
    if estado_orden_filtro != 'Todos':
        # Asume que el campo en el modelo es 'Estado'
        ordenes = ordenes.filter(Estado=estado_orden_filtro)

    # --- 3. SERIALIZAR LOS EVENTOS ---
    eventos = []
    for orden in ordenes:
        # Tu código existente para construir el diccionario de eventos:
        titulo_evento = f"OS-{orden.OrdenID} {orden.Servicio}"
        titulo_tooltip = f"#{orden.OrdenID} - {orden.ClienteEmpresa.NombreComercial}"

        eventos.append({
            'id': orden.OrdenID, 
            'title': titulo_evento, 
            'start': orden.Programada.isoformat(), 
            # Si tienes el campo de fin en el modelo, úsalo: 'end': orden.FinProgramada.isoformat(),
            'color': obtener_color_por_estado(orden.Estado), 
            'url': f'/app/ordenes/editar/{orden.OrdenID}/',
            
            'extendedProps': { 
                'cliente_nombre': orden.ClienteEmpresa.NombreComercial,
                'telefono': orden.TelefonoContacto,
                'ubicacion': orden.Ubicacion,
                'asignado': f"{orden.PersonalAsignado.Nombre} {orden.PersonalAsignado.Apellido}" if orden.PersonalAsignado else 'N/A',
                'estado_orden': orden.Estado,
                'tooltip_title': titulo_tooltip, 
                'servicio_detalle': orden.Servicio
            }
        })
        
    # Esta línea debe ser la última y estar correctamente sangrada
    return JsonResponse(eventos, safe=False)

def obtener_color_por_estado(estado):
    if estado == 'Pendiente':
        return '#f0ad4e'
    elif estado == 'En Proceso':
        return '#5bc0de'
    elif estado == 'Terminada':
        return '#5cb85c'
    elif estado == 'Cancelada':
        return '#d9534f'
    return '#777'



@login_required
def generar_registro(request, orden_id):
    # 🛑 RESTRICCIÓN: Solo Técnico (y Admin, si lo quieres)
    if request.user.Rol not in ['Administrador', 'Técnico']:
        messages.error(request, 'Acceso denegado. Solo personal técnico puede generar reportes.')
        return redirect('vista_calendario')
    
    # 1. Buscar la Orden de Servicio
    orden = get_object_or_404(OrdenesServicio, pk=orden_id)

    # 2. VERIFICAR si ya existe un registro
    # Si ya existe, no dejamos entrar de nuevo para no sobrescribir datos o tiempos.
    if RegistrosTecnicos.objects.filter(Orden=orden).exists():
        messages.warning(request, f"La Orden #{orden_id} ya tiene un registro técnico.")
        return redirect('lista_ordenes') 

    # --- ✅ NUEVO: REGISTRAR HORA DE INICIO ---
    # Al entrar a esta pantalla, significa que el técnico va a empezar a trabajar (o a reportar).
    # Si el campo 'Inicio' está vacío, guardamos la hora actual.
    if not orden.Inicio:
        orden.Inicio = timezone.localtime(timezone.now()).time()
        orden.save()
        print(f"🕒 Hora de Inicio guardada para la Orden #{orden.OrdenID}: {orden.Inicio}")
    # ------------------------------------------

    # 3. Preparar el contexto y mostrar la plantilla
    context = {
        'orden': orden,
    }

    return render(request, 'servicios/registro_tecnico.html', context)


@login_required
def guardar_registro_tecnico(request):
    # 🛑 RESTRICCIÓN: Solo Técnico 
    if request.user.Rol != 'Técnico':
        # Retorna error JSON porque es una API endpoint
        return JsonResponse({'status': 'error', 'message': 'Solo personal técnico puede guardar registros.'}, status=403)
    if request.method == 'POST':
        print("🔴 INICIO DEL PROCESO DE GUARDADO") 
        try:
            data = request.POST
            orden_id = data.get('orden_id')
            
            if not orden_id:
                return JsonResponse({'status': 'error', 'message': 'Falta la OrdenID.'}, status=400)
            
            try:
                orden = OrdenesServicio.objects.get(pk=orden_id)
            except OrdenesServicio.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'La Orden no existe.'}, status=404)

            # VERIFICAR SI YA EXISTE (Seguridad extra)
            if RegistrosTecnicos.objects.filter(Orden=orden).exists():
                 return JsonResponse({'status': 'error', 'message': 'Ya existe un registro para esta orden.'}, status=400)

            # 1. Crear el Registro (Datos de texto)
            registro = RegistrosTecnicos(
                Orden=orden,
                Tecnico=request.user,
                
                # Mapeo directo de campos
                TipoUnidad=data.get('tipoUnidad'),
                Marca=data.get('marca'),
                Modelo=data.get('modelo'),
                Capacidad=data.get('capacidad'),
                TipoGasRefrigerante=data.get('tipoGas'),
                InstalacionCondensador=data.get('condensador'),
                ServicioRealizado=data.get('servicio'),
                
                # Parámetros
                DistanciaEvap=data.get('distanciaEvapCond'),
                DistanciaAlimentacion=data.get('distanciaAlimentacion'),
                CalibreCableado=data.get('calibreAlimentacion'),
                TamanoHabitacion=data.get('tamanoHabitacion'),
                Desague=data.get('desague'),
                
                # Datos Técnicos
                PresionGasRefrig=data.get('presionGas'),
                VoltajeAlimentacion=data.get('voltajeAlimentacion'),
                VoltajeTerminalesCond=data.get('voltajeTerminales'),
                TempHabitacion=data.get('tempHabitacion'),
                TempDescarga=data.get('tempDescarga'),
                BombaVacio=data.get('bombaCFM'),
                TiempoVacio=data.get('bombaTiempo'),

                # Componentes
                CapacitorCompresor_Original=data.get('capCompOriginal'),
                CapacitorCompresor_Actual=data.get('capCompActual'),
                CapacitorVentilador_Original=data.get('capVentOriginal'),
                CapacitorVentilador_Actual=data.get('capVentActual'),
                AmpTerminalesCompresor_Original=data.get('ampCompOriginal'),
                AmpTerminalesCompresor_Actual=data.get('ampCompActual'),
                SensorPozo_Original=data.get('sensorPozoOriginal'),
                SensorPozo_Actual=data.get('sensorPozoActual'),
                SensorAmbiente_Original=data.get('sensorAmbienteOriginal'),
                SensorAmbiente_Actual=data.get('sensorAmbienteActual'),
                
                ObservacionesTexto=data.get('observacionesTexto'),
                Satisfaccion=data.get('satisfaccion') or None,
                ComentarioCliente=data.get('comentarioCliente'),
                NotasInternas=data.get('notasInternas'),
                
                FechaCreacion=timezone.now()
            )
            registro.save()
            print(f"✅ Registro base creado con ID: {registro.pk}")

            # 2. Materiales (JSON)
            materiales_json = data.get('materiales_json')
            if materiales_json:
                try:
                    registro.MaterialesUtilizados = json.loads(materiales_json)
                    registro.save(update_fields=['MaterialesUtilizados'])
                except:
                    print("⚠️ Error al guardar JSON de materiales")

            # 3. FIRMAS (Base64 -> Archivo)
            firma_cliente = data.get('firma_cliente_dataurl')
            firma_tecnico = data.get('firma_tecnico_dataurl')

            if firma_cliente and 'base64,' in firma_cliente:
                try:
                    fmt, imgstr = firma_cliente.split(';base64,')
                    ext = fmt.split('/')[-1]
                    archivo = ContentFile(base64.b64decode(imgstr), name=f'cliente_{registro.pk}.{ext}')
                    registro.FirmaCliente = archivo
                except Exception as e:
                    print(f"❌ Error firma cliente: {e}")

            if firma_tecnico and 'base64,' in firma_tecnico:
                try:
                    fmt, imgstr = firma_tecnico.split(';base64,')
                    ext = fmt.split('/')[-1]
                    archivo = ContentFile(base64.b64decode(imgstr), name=f'tecnico_{registro.pk}.{ext}')
                    registro.FirmaTecnico = archivo
                except Exception as e:
                    print(f"❌ Error firma técnico: {e}")
            
            registro.save() # Guardar cambios de firmas

# ---------------------------------------------------------
            # 5. FOTOS Y DESCRIPCIONES (ACTUALIZADO)
            # ---------------------------------------------------------
            archivos = request.FILES.getlist('fotos')
            descripciones = request.POST.getlist('descripciones') # <--- NUEVO: Recibimos la lista de textos
            
            print(f"📸 Procesando {len(archivos)} fotos con sus descripciones...")

            for i, foto in enumerate(archivos):
                # Obtenemos la descripción correspondiente a la foto (por posición)
                # Si el usuario no escribió nada, guardamos una cadena vacía
                texto_desc = descripciones[i] if i < len(descripciones) else ""
                
                RegistroFotos.objects.create(
                    Registro=registro,
                    Imagen=foto,
                    Descripcion=texto_desc # <--- AQUÍ SE GUARDA EN LA BD
                )
                print(f"   -> Foto {i+1} guardada: {texto_desc}")

            # ---------------------------------------------------------

            # 5. ACTUALIZAR ORDEN (Hora Fin y Estado)
            # Si Inicio no tenía hora (por error), le ponemos la de creación
            if not orden.Inicio:
                orden.Inicio = orden.Programada.time() if orden.Programada else timezone.now().time()
            
            orden.Fin = timezone.localtime(timezone.now()).time()
            orden.Estado = 'Terminada'
            orden.save()
            print(f"✅ Orden finalizada a las {orden.Fin}")

            return JsonResponse({'status': 'success', 'message': 'Registro guardado exitosamente.', 'id': registro.pk})
            #return redirect('generar_y_abrir_pdf', orden_id=nueva_orden.OrdenID)
        
        except Exception as e:
            print(f"❌ ERROR CRÍTICO: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)
    
@login_required 
def lista_reportes_pendientes_view(request):
    # 🛑 RESTRICCIÓN: Solo Administrador y Técnico
    if request.user.Rol not in ['Administrador', 'Técnico']:
        messages.error(request, 'Acceso denegado.')
        return redirect('vista_calendario')
    # 1. Obtener la query de búsqueda
    query = request.GET.get('q')
    
    # 2. QuerySet base (Órdenes Pendientes)
    ordenes_con_reporte = RegistrosTecnicos.objects.values_list('Orden_id', flat=True)
    
    ordenes = OrdenesServicio.objects.filter(
        Estado='Pendiente'
    ).exclude(
        OrdenID__in=ordenes_con_reporte
    ).select_related('ClienteEmpresa', 'PersonalAsignado').order_by('Programada')

    # 3. Aplicar filtro de búsqueda
    if query:
        # Filtramos por Cliente, Folio (OrdenID) o Servicio
        ordenes = ordenes.filter(
            Q(ClienteEmpresa__NombreComercial__icontains=query) |
            Q(OrdenID__icontains=query) |                          
            Q(Servicio__icontains=query)
        ).distinct()

    contexto = {
        'ordenes_pendientes': ordenes,
        'search_query': query if query else '', # ✅ Para mantener el texto buscado en el input
    }
    
    return render(request, 'servicios/lista_reportes_pendientes.html', contexto)



def link_callback(uri, rel):
    """
    Convierte URLs de HTML a rutas utilizables por xhtml2pdf.
    Soporta URLs firmadas de S3, Base64 (QR) y archivos estáticos locales (Logo).
    """
    uri = uri.strip()

    # 1. Si es una URL de internet (S3 con firma), la devolvemos intacta.
    # Esto permite que xhtml2pdf descargue la imagen usando el token de seguridad.
    if uri.lower().startswith('http') or uri.startswith('//'):
        return uri

    # 2. Si es una imagen Base64 (Códigos QR), la dejamos pasar intacta.
    if uri.startswith('data:'):
        return uri

    # 3. Manejo de archivos ESTÁTICOS locales (como el LOGO)
    sUrl = settings.STATIC_URL        # Generalmente '/static/'
    sRoot = settings.STATIC_ROOT      # Carpeta donde Render guarda estáticos recopilados
    
    path = uri # Valor por defecto

    if uri.startswith(sUrl):
        clean_uri = uri.replace(sUrl, "")
        
        # A) Buscar en STATIC_ROOT (Ruta de producción en Render)
        if sRoot:
            path = os.path.join(sRoot, clean_uri)
        
        # B) Si no existe en root, buscar en la carpeta static del proyecto
        if not os.path.isfile(path):
             path = os.path.join(settings.BASE_DIR, 'static', clean_uri)
             
        # C) Búsqueda específica en la carpeta de la app
        if not os.path.isfile(path):
            path = os.path.join(settings.BASE_DIR, 'servicios', 'static', clean_uri)

    # 4. Normalizar la ruta (importante para evitar errores de barras)
    path = os.path.normpath(path)

    # 5. DEPURACIÓN DE LOGO (Opcional, útil para ver si Render encuentra el logo)
    if "logo" in str(uri).lower():
        print(f"\n🔍 --- DEPURACIÓN DE LOGO ---")
        print(f" 1. URI recibida: {uri}")
        print(f" 2. Ruta final en disco: {path}")
        print(f" 3. ¿Existe el archivo?: {os.path.isfile(path)}")
        print(f"------------------------------\n")

    # 6. Verificación final para archivos locales
    # Si NO es una URL de internet y el archivo físico no existe, devolvemos None
    if not uri.lower().startswith('http') and not os.path.isfile(path):
        print(f"⚠️ AVISO PDF: No se encontró la imagen local: {path}")
        return None 

    return path

@login_required
def ver_reporte_view(request, orden_id):
    try:
        # 1. Obtener datos de la base de datos
        orden = get_object_or_404(OrdenesServicio, pk=orden_id)
        reporte = get_object_or_404(RegistrosTecnicos, Orden=orden)
        fotos = RegistroFotos.objects.filter(Registro=reporte)
        items_orden = OrdenDetalles.objects.filter(Orden=orden)

        # 2. Generar Código QR en Memoria (Sin internet)
        qr_content = f"Orden-{orden.OrdenID} | Cliente: {orden.ClienteEmpresa.NombreComercial}"
        qr_img = qrcode.make(qr_content)
        
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        qr_url_final = f"data:image/png;base64,{qr_base64}"

   # --- ✅ NUEVO: BÚSQUEDA INTELIGENTE DEL LOGO ---
# --- ✅ SOLUCIÓN FINAL: CONVERTIR LOGO A BASE64 ---
        # 1. Definir la ruta (ya sabemos que esta ruta es correcta gracias a tu log)
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.jpeg')
        
        # 2. Si no está ahí, probar en la carpeta de la app
        if not os.path.exists(logo_path):
            logo_path = os.path.join(settings.BASE_DIR, 'servicios', 'static', 'img', 'logo.jpeg')

        logo_data = None
        
        if os.path.exists(logo_path):
            try:
                with open(logo_path, "rb") as image_file:
                    # Leemos los bytes y los convertimos a texto
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    # Creamos la cadena que entiende el HTML
                    logo_data = f"data:image/jpeg;base64,{encoded_string}"
                    print("✅ LOGO CONVERTIDO A CÓDIGO EXITOSAMENTE")
            except Exception as e:
                print(f"❌ Error al leer el logo: {e}")
        else:
            print(f"❌ ERROR: Archivo no encontrado en: {logo_path}")
        # -------------------------------------------

        context = {
            'orden': orden,
            'reporte': reporte,
            'fotos': fotos,
            'items': items_orden,
            'qr_url': qr_url_final,
            'logo_url': logo_data,  # <--- Enviamos el CÓDIGO de la imagen, no la ruta
        }
        
        # 4. Renderizar HTML
        template = get_template('servicios/Reporte_Orden_S.html')
        html = template.render(context)

        # 5. Generar PDF
        response = HttpResponse(content_type='application/pdf')
        # Si quieres que se descargue directo, descomenta la siguiente línea:
        # response['Content-Disposition'] = f'attachment; filename="Reporte_{orden_id}.pdf"'
        
        pisa_status = pisa.CreatePDF(
            html,
            dest=response,
            link_callback=link_callback # Usamos la función que ya arreglamos
        )

        if pisa_status.err:
            return HttpResponse('Hubo un error al generar el PDF <pre>' + html + '</pre>')
        
        return response
        
    except RegistrosTecnicos.DoesNotExist:
        messages.error(request, f"La orden #{orden_id} aún no tiene un reporte técnico.")
        return redirect('lista_ordenes')



def login_view(request):
    template_name = 'servicios/login.html' 
    
    # 1. Bloque de Redirección para Usuarios YA AUTENTICADOS (Acceso directo a /login/)
    if request.user.is_authenticated:
        if request.user.Rol == 'Administrador':
            # ➡️ Administrador va a Gestión de Usuarios (Control Total)
            return redirect('gestion_usuarios')
        elif request.user.Rol == 'Técnico':
            # 🚀 Técnico va a Reportes Pendientes (Su tarea principal)
            return redirect('lista_reportes_pendientes')
        else:
            # ➡️ Otros roles (Soporte/Consultor) van al Calendario (Solo consulta)
            return redirect('vista_calendario') 

    
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            # 2. ¡AUTENTICACIÓN EXITOSA! Iniciamos la sesión
            login(request, user) 
            
            # --- REDIRECCIÓN BASADA EN ROL ---
            if user.Rol == 'Administrador':
                messages.success(request, f"Bienvenido, Administrador {user.Nombre}.")
                return redirect('vista_calendario')
            elif user.Rol == 'Técnico':
                # 🚀 Técnico redirigido a Generar Reporte
                messages.success(request, f"Bienvenido, {user.Rol} {user.Nombre}. Acceso a Reportes.")
                return redirect('vista_calendario')
            else:
                # ➡️ Otros roles (Consultor/Soporte)
                messages.success(request, f"Bienvenido, {user.Rol} {user.Nombre}.")
                return redirect('vista_calendario') 
        else:
            # 3. Autenticación fallida
            messages.error(request, 'Correo electrónico o contraseña incorrectos.')
            
    # Si es GET o la autenticación falló, renderiza el template de login
    return render(request, template_name)

def logout_view(request):
    """
    Cierra la sesión del usuario actual y lo redirige al login.
    """
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    # Redirige a la URL nombrada 'login' (la que tienes en urls.py)
    return redirect('login')

    # ----------------------------------------------------------------------
# VISTA DE LOGIN (LISTA PARA PRODUCCIÓN CON REDIRECCIÓN POR ROL)
# ----------------------------------------------------------------------
# ... (tu login_view) ...

# ----------------------------------------------------------------------
# VISTA DE LOGOUT
# ----------------------------------------------------------------------
# ... (tu logout_view) ...


# ----------------------------------------------------------------------
# VISTA DE API PARA AUTOCOMPLETAR CLIENTES (CORREGIDA)
# ----------------------------------------------------------------------
@login_required
def get_client_details(request, cliente_id):
    try:
        # 1. Buscar el cliente usando el ID que se pasó
        cliente = Clientes.objects.get(pk=cliente_id)
        
        # 2. OBTENER EL LINK DE UBICACIÓN
        # Aquí está el cambio: Ya no unimos calle y colonia.
        # Simplemente leemos el campo 'Ubicacion' donde guardaste el link.
        # Si está vacío, mandamos una cadena vacía ('').
        link_mapa = cliente.Ubicacion if cliente.Ubicacion else ''
        
        # 3. Preparar los datos para enviar como JSON
        data = {
            'telefono': cliente.Telefono,
            'email': cliente.Correo,
            'ubicacion': link_mapa  # <--- Enviamos el link directo
        }
        return JsonResponse(data)
        
    except Clientes.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)
    

def enviar_notificacion_telegram(orden):
    """Envía una notificación al grupo de Telegram al crear o actualizar una orden."""
    
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    url_base = f"https://api.telegram.org/bot{bot_token}/sendMessage"

      # --- 1. LÓGICA PARA OBTENER Y FORMATEAR MATERIALES (NUEVO BLOQUE) ---
    detalles = orden.ordendetalles_set.all() # Consulta los detalles relacionados
    
    materiales_lista = ""
    if detalles:
        materiales_lista = "\n📦 Materiales Utilizados: \n"
        for detalle in detalles:
            # Formato: • [CANTIDAD] [PRODUCTO] (Información Adicional)
            info_adicional = f" ({detalle.InformacionAdicional})" if detalle.InformacionAdicional else ""
            materiales_lista += f"  • {detalle.Cantidad} x {detalle.Producto}{info_adicional}\n"
    else:
        materiales_lista = "\n📦 Materiales: (No se agregaron productos/materiales.)\n"
    # --- FIN DE LA LÓGICA DE MATERIALES ---

    # --- ATENCIÓN AQUÍ: Debes usar la URL completa ---
    # Si estás en desarrollo (localhost), debes usar http://127.0.0.1:8000
    # Si estás en producción, debes usar tu dominio (ej. https://itech.com)
    
    # Asumimos que estás en desarrollo por ahora (cámbialo si es producción):
    dominio_base = "http://127.0.0.1:8000" 
    
    try:
        orden_link = f"{dominio_base}{reverse('editar_orden', args=[orden.OrdenID])}"
    except Exception as e:
        # En caso de que la URL reverse falle
        orden_link = f"(Error al generar URL: {e})"
        print(f"DEBUG: Error al generar URL para Telegram: {e}") 

    # 2. Construir el mensaje (Usando Markdown)
    mensaje = (
        f"🚨 *NUEVA ORDEN DE SERVICIO ASIGNADA* 🚨\n\n"
        f"📋 *Folio:* **#{orden.OrdenID}**\n"
        f"🏢 *Cliente:* {orden.ClienteEmpresa.NombreComercial}\n"
        f"🧑‍🔧 *Técnico:* {orden.PersonalAsignado.Nombre} {orden.PersonalAsignado.Apellido}\n"
        f"📅 *Programada:* {orden.Programada.strftime('%d/%m/%Y %H:%M')}\n"
        f"📍 *Ubicación:* [Abrir en Maps]({orden.Ubicacion})\n"
        f"🛠️ *Servicio:* {orden.Servicio}\n"
        f"📝 *Falla Reportada:* {orden.FallaReportada[:100]}...\n"
        f"{materiales_lista}\n\n" # <-- LISTA DE MATERIALES AÑADIDA
        f"🔗 [Ver Detalles de la Orden]({orden_link})"
    )

    # 3. Preparar y enviar la solicitud
    payload = {
        'chat_id': chat_id,
        'text': mensaje,
        'parse_mode': 'Markdown',
    }

    try:
        response = requests.post(url_base, data=payload)
        response.raise_for_status() 
        # --- AÑADE ESTE LOG DE DEBUG (CONFIRMACIÓN) ---
        print(f"TELEGRAM SUCCESS: Orden #{orden.OrdenID} notificada.")
        # -----------------------------------------------
    except requests.exceptions.RequestException as e:
        # --- LOG DE ERROR PARA VER POR QUÉ FALLÓ ---
        print(f"TELEGRAM ERROR: No se pudo notificar la Orden #{orden.OrdenID}. Razón: {e}")

        # ----------------------------------------------------------------------
# FUNCIONES DE AYUDA (CONTROL DE ACCESO)
# ----------------------------------------------------------------------

def check_admin_only(request):
    # ...
    if request.user.Rol == 'Administrador':
        return None # Acceso permitido

    messages.error(request, 'Acceso denegado. No tienes permisos para esta sección.')
    
    if request.user.Rol == 'Técnico':
        return redirect('lista_reportes_pendientes') 
    
    # 🚀 Soporte y otros roles no permitidos son redirigidos aquí.
    return redirect('vista_calendario')

@login_required
def generar_y_abrir_pdf(request, orden_id):
    try:
        orden = get_object_or_404(OrdenesServicio, pk=orden_id)
        
        # ⚠️ Si tu PDF se llama Reporte_Orden_S.html, asegúrate que pueda renderizar SOLO la orden.
        # Si esta plantilla requiere el RegistroTecnico, la generación fallará aquí
        # porque el reporte técnico aún no se ha creado.
        template = get_template('servicios/Reporte_Orden_S.html') 
        context = {'orden': orden} # Agrega aquí más datos si tu PDF los requiere
        html = template.render(context)

        # 🚀 Generar PDF y forzar la apertura
        response = HttpResponse(content_type='application/pdf')
        # 'inline' fuerza al navegador a intentar mostrarlo en lugar de descargarlo
        response['Content-Disposition'] = f'inline; filename="Orden_Servicio_{orden_id}.pdf"' 
        
        pisa.CreatePDF(
            html,
            dest=response,
            link_callback=link_callback 
        )
        
        return response
    
    except Exception as e:
        messages.error(request, f"Error al generar el PDF de la orden: {e}")
        return redirect('lista_ordenes')