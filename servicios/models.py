from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import Q # Necesario para el backend

# --- CONSTANTES DE ROL (DEFINIDAS AL INICIO PARA VISIBILIDAD) ---
ROL_ADMIN = 'Administrador'
ROL_TECNICO = 'Técnico'
ROL_SOPORTE = 'Soporte'
ROLES_CHOICES = [
    (ROL_ADMIN, 'Administrador'),
    (ROL_TECNICO, 'Técnico'),
    (ROL_SOPORTE, 'Soporte/Oficina'),
]
# ------------------------------------------------------------------
# --- CONSTANTES DE GIRO (NECESARIO PARA QUE OrdenesServicio LAS VEA) ---
GIRO_ENERGIA = 'Energia'
GIRO_RESIDENCIAL = 'Servicios residencial'
GIRO_COMERCIAL = 'Linea comercial'
GIRO_INDUSTRIAL = 'Linea industrial'
GIRO_REFRIGERACION = 'Unidades de refrigeración'
GIRO_ELECTROGENOS = 'Equipos electrogenos'

GIROS_CHOICES = [
    (GIRO_ENERGIA, 'Energia'),
    (GIRO_RESIDENCIAL, 'Servicios residencial'),
    (GIRO_COMERCIAL, 'Linea comercial'),
    (GIRO_INDUSTRIAL, 'Linea industrial'),
    (GIRO_REFRIGERACION, 'Unidades de refrigeración'),
    (GIRO_ELECTROGENOS, 'Equipos electrogenos'),
]
# ----------------- MANAGER PERSONALIZADO -----------------
class UsuarioManager(BaseUserManager):
    def create_user(self, correo_electronico, password=None, nombre=None, apellido=None, **extra_fields):
        if not correo_electronico:
            raise ValueError('El usuario debe tener un correo electrónico')

        user = self.model(
            CorreoElectronico=self.normalize_email(correo_electronico),
            # Nombre=nombre,          <-- ¡Línea ELIMINADA!
            # Apellido=apellido,      <-- ¡Línea ELIMINADA!
            **extra_fields          # ⬅️ Ahora esto asigna Nombre, Apellido, Rol, etc.
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

# Dentro de class UsuarioManager(BaseUserManager):
    # ... (código de create_user)

    def create_superuser(self, correo_electronico, password=None, **extra_fields):
        # Esta lógica crea el usuario y establece las propiedades después
        
        is_staff_val = extra_fields.pop('is_staff', True)
        is_superuser_val = extra_fields.pop('is_superuser', True)
        
        extra_fields.setdefault('Rol', ROL_ADMIN)
        extra_fields.setdefault('Nombre', 'Admin') 
        extra_fields.setdefault('Apellido', 'Master') 
        
        # 1. Crear el usuario (Nombre, Apellido, Rol, etc., se pasan vía extra_fields)
        user = self.create_user(correo_electronico, password, **extra_fields)

        # 2. Asignar las propiedades que causaban error 'no setter' DESPUÉS
        user.is_staff = is_staff_val
        user.is_superuser = is_superuser_val
        user.save(using=self._db) # Guardar los cambios finales
        return user

# ----------------- MODELO DE USUARIO PERSONALIZADO -----------------
class Usuarios(AbstractBaseUser):
    # CAMPOS DE TU TABLA ORIGINAL
    UsuarioID = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=100) 
    Apellido = models.CharField(max_length=100)
    NumeroTelefono = models.CharField(max_length=20, blank=True, null=True)
    CorreoElectronico = models.EmailField(unique=True, max_length=255)
    Rol = models.CharField(max_length=50, choices=ROLES_CHOICES, default=ROL_TECNICO) 
    
    # CAMPOS REQUERIDOS POR DJANGO
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False) 

    # Define tu manager
    objects = UsuarioManager()

    # Campos de login que Django usará:
    USERNAME_FIELD = 'CorreoElectronico' # Usaremos el Correo como identificador ÚNICO principal
    EMAIL_FIELD = 'CorreoElectronico' 
    REQUIRED_FIELDS = ['Nombre', 'Apellido'] # Campos que se piden al crear un superusuario


    # --- Permisos y Propiedades (Controlados por Rol) ---
    @property
    def is_staff(self):
        return self.Rol == ROL_ADMIN
    @property
    def is_superuser(self):
        return self.Rol == ROL_ADMIN
    def has_perm(self, perm, obj=None):
        return self.Rol == ROL_ADMIN
    def has_module_perms(self, app_label):
        return self.Rol == ROL_ADMIN

    def __str__(self):
        return f"{self.Nombre} {self.Apellido}"

    class Meta:
        db_table = 'Usuarios'

# ------------------------------------------------------------------
# [CLIENTES]
# ------------------------------------------------------------------

class Clientes(models.Model):
    ClienteID = models.AutoField(primary_key=True)
    NombreComercial = models.CharField(max_length=255)
    Telefono = models.CharField(max_length=20, blank=True, null=True)
    Correo = models.CharField(max_length=255, blank=True, null=True)
    Calle = models.CharField(max_length=255, blank=True, null=True)
    NumeroExterior = models.CharField(max_length=20, blank=True, null=True)
    Interior = models.CharField(max_length=20, blank=True, null=True)
    Colonia = models.CharField(max_length=100, blank=True, null=True)
    CodigoPostal = models.CharField(max_length=10, blank=True, null=True)
    Ciudad = models.CharField(max_length=100, blank=True, null=True)
    Pais = models.CharField(max_length=100, blank=True, null=True)
    Ubicacion = models.TextField(verbose_name="Enlace Google Maps", blank=True, null=True)

    class Meta:
        db_table = 'Clientes'

    def __str__(self):
        return self.NombreComercial


class OrdenesServicio(models.Model):
    ESTADO_PENDIENTE = 'Pendiente'
    ESTADO_TERMINADA = 'Terminada'
    ESTADOS_CHOICES = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_TERMINADA, 'Terminada'),
    ]
    OrdenID = models.AutoField(primary_key=True)
    ClienteEmpresa = models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True, db_column='ClienteEmpresaID')
    TelefonoContacto = models.CharField(max_length=20, blank=True, null=True)
    EmailContacto = models.CharField(max_length=255, blank=True, null=True)
    Servicio = models.CharField(max_length=255, blank=True, null=True)
    # Filtro para solo mostrar técnicos y usamos el rol
    PersonalAsignado = models.ForeignKey(
        Usuarios, 
        on_delete=models.SET_NULL, 
        null=True, 
        db_column='PersonalAsignadoID', 
        limit_choices_to={'Rol': ROL_TECNICO}
    )
    Giro = models.CharField(
        max_length=100, 
        choices=GIROS_CHOICES, 
        blank=True, null=True # <--- CAMBIO: Sin default, permite vacío
    )
    Ubicacion = models.CharField(max_length=255, blank=True, null=True)
    FallaReportada = models.TextField(blank=True, null=True)
    Programada = models.DateTimeField(blank=True, null=True)
    Precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    Estado = models.CharField(
        max_length=50,
        choices=ESTADOS_CHOICES,
        default=ESTADO_PENDIENTE
    )
    # ✅ AGREGA ESTAS DOS LÍNEAS:
    Inicio = models.TimeField(blank=True, null=True, verbose_name="Hora Inicio Real")
    Fin = models.TimeField(blank=True, null=True, verbose_name="Hora Fin Real")

    class Meta:
        db_table = 'OrdenesServicio'

    def __str__(self):
        return f"Orden #{self.OrdenID} - {self.Servicio}"


class Actividades(models.Model):
    ActividadID = models.AutoField(primary_key=True)
    Titulo = models.CharField(max_length=255, blank=True, null=True)
    Cliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True, db_column='ClienteID')
    Descripcion = models.TextField(blank=True, null=True)
    Fecha = models.DateField(blank=True, null=True)
    Inicio = models.TimeField(blank=True, null=True)
    Fin = models.TimeField(blank=True, null=True)
    PersonalAsignado = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True, db_column='PersonalAsignadoID')
    Estado = models.CharField(max_length=50, blank=True, null=True)
    Ubicacion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Actividades'


class OrdenDetalles(models.Model):
    DetalleID = models.AutoField(primary_key=True)
    Orden = models.ForeignKey(OrdenesServicio, on_delete=models.CASCADE, db_column='OrdenID')
    Cantidad = models.IntegerField(blank=True, null=True)
    Producto = models.CharField(max_length=255, blank=True, null=True)
    InformacionAdicional = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'OrdenDetalles'


# ===================================================================
# REGISTRO TÉCNICO PRINCIPAL (RegistrosTecnicos)
# ===================================================================
class RegistrosTecnicos(models.Model):
    RegistroID = models.AutoField(primary_key=True)
    # Enlazar con la Orden a la que pertenece este registro
    Orden = models.OneToOneField(OrdenesServicio, on_delete=models.CASCADE, db_column='OrdenID')
    
    # Campo para enlazar al Técnico que lo generó (basado en Usuarios)
    Tecnico = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True, db_column='TecnicoID', related_name='registros_generados')
    
    # ===================================================================
    # 1. Datos del Equipo
    # ===================================================================
    TipoUnidad = models.CharField(max_length=100, blank=True, null=True)
    Marca = models.CharField(max_length=100, blank=True, null=True)
    Modelo = models.CharField(max_length=100, blank=True, null=True)
    Capacidad = models.CharField(max_length=100, blank=True, null=True)
    TipoGasRefrigerante = models.CharField(max_length=50, blank=True, null=True)
    InstalacionCondensador = models.CharField(max_length=100, blank=True, null=True)
    ServicioRealizado = models.CharField(max_length=255, blank=True, null=True)
    
    # ===================================================================
    # 2, 3, 4. Parámetros, Lecturas y Componentes
    # ===================================================================
    DistanciaEvap = models.CharField(max_length=50, blank=True, null=True)
    DistanciaAlimentacion = models.CharField(max_length=50, blank=True, null=True)
    CalibreCableado = models.CharField(max_length=50, blank=True, null=True)
    TamanoHabitacion = models.CharField(max_length=50, blank=True, null=True)
    Desague = models.CharField(max_length=100, blank=True, null=True)
    PresionGasRefrig = models.CharField(max_length=50, blank=True, null=True)
    VoltajeAlimentacion = models.CharField(max_length=50, blank=True, null=True)
    VoltajeTerminalesCond = models.CharField(max_length=50, blank=True, null=True)
    TempHabitacion = models.CharField(max_length=50, blank=True, null=True)
    TempDescarga = models.CharField(max_length=50, blank=True, null=True)
    BombaVacio = models.CharField(max_length=50, blank=True, null=True)
    TiempoVacio = models.CharField(max_length=50, blank=True, null=True)
    CapacitorCompresor_Original = models.CharField(max_length=50, blank=True, null=True)
    CapacitorCompresor_Actual = models.CharField(max_length=50, blank=True, null=True)
    CapacitorVentilador_Original = models.CharField(max_length=50, blank=True, null=True)
    CapacitorVentilador_Actual = models.CharField(max_length=50, blank=True, null=True)
    AmpTerminalesCompresor_Original = models.CharField(max_length=50, blank=True, null=True)
    AmpTerminalesCompresor_Actual = models.CharField(max_length=50, blank=True, null=True)
    SensorPozo_Original = models.CharField(max_length=50, blank=True, null=True)
    SensorPozo_Actual = models.CharField(max_length=50, blank=True, null=True)
    SensorAmbiente_Original = models.CharField(max_length=50, blank=True, null=True)
    SensorAmbiente_Actual = models.CharField(max_length=50, blank=True, null=True)
    
    # ===================================================================
    # 5. CAMPOS NUEVOS (OBSERVACIONES Y MATERIALES)
    # ===================================================================
    ObservacionesTexto = models.TextField(max_length=6000, blank=True, null=True)
    Satisfaccion = models.IntegerField(blank=True, null=True) # 1-10
    ComentarioCliente = models.TextField(blank=True, null=True)
    NotasInternas = models.TextField(blank=True, null=True)
    
    # Se añade null=True porque creaste la columna JSON manualmente como NULL.
    MaterialesUtilizados = models.JSONField(blank=True, null=True)
    
    # ===================================================================
    # 6. CAMPOS NUEVOS (FIRMAS)
    # ===================================================================
    FirmaCliente = models.ImageField(upload_to='firmas/clientes/', blank=True, null=True)
    FirmaTecnico = models.ImageField(upload_to='firmas/tecnicos/', blank=True, null=True)
    
    # CORRECCIÓN: auto_now_add no soporta null=True. Para evitar conflictos con la columna 
    # NULL que creaste en la BD, se añade 'null=True' para la inserción y se quita auto_now_add.
    # La vista lo puede manejar con timezone.now() o puedes dejarlo auto_now_add si la BD lo maneja.
    FechaCreacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'registrostecnicos' # Nombre de la tabla en MySQL
        
    def __str__(self):
        return f"Registro #{self.RegistroID} - Orden {self.Orden.OrdenID}"


# ===================================================================
# REGISTRO DE FOTOS (RegistroFotos)
# ===================================================================
class RegistroFotos(models.Model):
    FotoID = models.AutoField(primary_key=True)
    Registro = models.ForeignKey(RegistrosTecnicos, related_name='fotos', on_delete=models.CASCADE)
    Imagen = models.ImageField(upload_to='fotos/registros/')
    Descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # Si ejecutaste la sentencia SQL para este modelo, usa el mismo nombre
        db_table = 'RegistroFotos'