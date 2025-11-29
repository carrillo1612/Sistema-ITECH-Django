from django import forms
from .models import Clientes,OrdenesServicio, Usuarios,RegistrosTecnicos 


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        # Especifica los campos de tu modelo que el formulario va a usar
        fields = [
            'NombreComercial', 
            'Telefono', 
            'Correo', 
            'Calle',
            'NumeroExterior',
            'Interior',
            'Colonia',
            'CodigoPostal', # Tu HTML lo llama 'cp', lo ajustaremos
            'Ciudad',
            'Pais', 
            'Ubicacion'
            # Puedes añadir más campos del modelo aquí si están en tu modal
        ]

        # ✅ AGREGAMOS EL DICCIONARIO WIDGETS AQUÍ
        widgets = {
            'Telefono': forms.TextInput(attrs={
                'class': 'form-control',      # O la clase de estilo que uses (ej: input-style)
                'maxlength': '10',            # Límite físico de caracteres
                'minlength': '10',            # Mínimo esperado
                'pattern': '[0-9]{10}',        # Patrón estricto: 10 dígitos exactos
                'title': 'Debe introducir 10 números exactos',
                'oninput': "this.value = this.value.replace(/[^0-9]/g, '');", # Solo permite números
                'placeholder': '10 dígitos'
            }),
        }
# ✅ 2. VALIDACIÓN DE SERVIDOR (SEGURIDAD)
    def clean_Telefono(self):
        numero = self.cleaned_data.get('Telefono')
        # Si el usuario escribió algo, verificamos que sean exactamente 10 dígitos
        if numero and len(numero) != 10:
            raise forms.ValidationError("El teléfono debe tener exactamente 10 dígitos.")
        return numero


class OrdenServicioForm(forms.ModelForm):
# 1. DEFINIMOS LAS OPCIONES DE SERVICIO
    OPCIONES_SERVICIO = [
        ('', 'Selecciona un servicio...'), # Opción vacía por defecto
        ('Mantenimiento', 'Mantenimiento'),
        ('Revisión', 'Revisión'),
        ('Reparación', 'Reparación'),
        ('Instalación', 'Instalación'),
        ('Diagnóstico', 'Diagnóstico'),
        ('Garantía', 'Garantía'),
    ]

    # 2. TRANSFORMAMOS EL CAMPO DE TEXTO A SELECT
    Servicio = forms.ChoiceField(
        choices=OPCIONES_SERVICIO,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Servicio *'
    )

    # Constructor para obligar que el Giro no esté vacío
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Giro'].required = True
    class Meta:
        model = OrdenesServicio
        fields = [
            'ClienteEmpresa', 
            'TelefonoContacto', 
            'EmailContacto', 
            'Servicio', 
            'PersonalAsignado', 
            'Giro', 
            'Ubicacion', 
            'FallaReportada', 
            'Programada', 
            'Precio',
            'Estado',
        ]
        
        widgets = {
            'ClienteEmpresa': forms.Select(attrs={'class': 'form-control'}),
            'PersonalAsignado': forms.Select(attrs={'class': 'form-control'}),
            'Estado': forms.Select(attrs={'class': 'form-control'}),

            # ✅ AQUÍ ES DONDE VA LA VALIDACIÓN DEL TELÉFONO:
            'TelefonoContacto': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '10',       # Límite de caracteres
                'minlength': '10',       # Mínimo (opcional)
                # ✅ CAMBIO 1: Este patrón obliga a que sean EXACTAMENTE 10 números
                'pattern': '[0-9]{10}', 
                'title': 'Debe introducir 10 números exactos',
                'oninput': "this.value = this.value.replace(/[^0-9]/g, '');",
                'placeholder': '10 dígitos'
            }),
            
            # ✅ AGREGAMOS ESTO AQUÍ PARA ACTIVAR EL CALENDARIO:
            'Programada': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',  # <--- ESTO ACTIVA EL CALENDARIO
                    'class': 'form-control'
                },
                format='%Y-%m-%dT%H:%M' # Formato necesario para que el calendario entienda la fecha
            ),
        }

        # ✅ VALIDACIÓN DE TELÉFONO (BACKEND / SERVIDOR)
    # Esto evita que se guarde si alguien burla la seguridad del navegador
    def clean_TelefonoContacto(self):
        numero = self.cleaned_data.get('TelefonoContacto')
        if numero and len(numero) != 10:
            raise forms.ValidationError("El teléfono debe tener exactamente 10 dígitos.")
        return numero

# En servicios/forms.py

class UsuarioForm(forms.ModelForm):
    # 1. Definición especial del campo 'password' para edición/creación
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Dejar en blanco para no cambiar'}), 
        required=False,
        label='Contraseña (Temporal / Nueva)'
    )

    class Meta:
        model = Usuarios
        fields = [
            'Nombre', 
            'Apellido', 
            'NumeroTelefono', 
            'CorreoElectronico', 
            'Rol',
        ]
        
        # Validación de frontend para NumeroTelefono (se mantiene)
        widgets = {
            'NumeroTelefono': forms.TextInput(attrs={
                'class': 'form-control', 
                'maxlength': '10', 
                'minlength': '10', 
                'pattern': '[0-9]{10}', 
                'title': 'Debe introducir 10 números exactos',
                'oninput': "this.value = this.value.replace(/[^0-9]/g, '');",
                'placeholder': '10 dígitos'
            }),
        }


    # 🚀 PARTE CLAVE: EL CONSTRUCTOR __init__
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 1. Iterar sobre todos los campos para aplicar REQUIRED y estilos
        for field_name, field in self.fields.items():
            
            # Aplicar estilos genéricos a todos los widgets de entrada
            field.widget.attrs.update({
                # Usa 'form-control' si esa es la clase que le da estilo en tu proyecto
                'class': 'form-control', 
                # Aseguramos que los campos se marquen como obligatorios en el HTML
                'required': 'required'
            })

        # 2. Reafirmar la obligatoriedad de los campos específicos (si es necesario)
        self.fields['Nombre'].required = True
        self.fields['Apellido'].required = True
        self.fields['CorreoElectronico'].required = True
        self.fields['NumeroTelefono'].required = True
        
        # 3. CONFIGURACIÓN DEL CAMPO ROL (La solución a tu problema)
        # Esto le dice a Django que debe renderizar una opción vacía por defecto
        # para que el usuario se vea forzado a seleccionar un valor.
        if 'Rol' in self.fields:
            self.fields['Rol'].required = True
            # ESTO HACE QUE APAREZCA EL TEXTO DE SELECCIÓN POR DEFECTO:
            self.fields['Rol'].empty_label = "--- Seleccione el Rol ---"

# ✅ AQUÍ AGREGAMOS LA VALIDACIÓN DE TELÉFONO
        widgets = {
            'NumeroTelefono': forms.TextInput(attrs={
                'class': 'form-control',      # O 'input-style' si estás usando Tailwind en esa pantalla
                'maxlength': '10',            # No deja escribir más de 10
                'minlength': '10',            # Pide mínimo 10
                # ✅ CAMBIO 1: Este patrón obliga a que sean EXACTAMENTE 10 números
                'pattern': '[0-9]{10}', 
                'title': 'Debe introducir 10 números exactos',
                'oninput': "this.value = this.value.replace(/[^0-9]/g, '');",
                'placeholder': '10 dígitos'
            }),
            

        }

    # ... (tu método save sigue igual) ...

    # ✅ CAMBIO 2: AGREGAR ESTA FUNCIÓN DE VALIDACIÓN
    # Django ejecuta esto automáticamente antes de guardar.
    def clean_NumeroTelefono(self):
        numero = self.cleaned_data.get('NumeroTelefono')
        # Si el usuario escribió algo, verificamos la longitud
        if numero and len(numero) != 10:
            raise forms.ValidationError("El teléfono debe tener exactamente 10 dígitos.")
        return numero

    # Sobreescribimos el save para hashear la contraseña
    def save(self, commit=True):
        usuario = super(UsuarioForm, self).save(commit=False)
        
        # Obtenemos el valor del campo 'password' del formulario
        contrasena_plana = self.cleaned_data.get("password") 
        
        # Solo hashea y asigna si se proporcionó una contraseña
        if contrasena_plana:
            # Dado que Usuarios hereda de AbstractBaseUser, este método existe y hashea correctamente.
            usuario.set_password(contrasena_plana)
        
        # Si no se proporcionó contraseña, el hash existente se mantiene automáticamente.

        if commit:
            usuario.save()
        return usuario

class RegistroTecnicoForm(forms.ModelForm):
    class Meta:
        model = RegistrosTecnicos
        # Incluye todos los campos de RegistrosTecnicos
        fields = '__all__'
        
        widgets = {
            # Se usarán inputs de texto para casi todos los campos VARCHAR/CharField
            # Puedes añadir más placeholders aquí si lo deseas
            'TipoUnidad': forms.TextInput(attrs={'placeholder': 'Ej: Mini Split'}),
            'Marca': forms.TextInput(attrs={'placeholder': 'Ej: Carrier'}),
            'Capacidad': forms.TextInput(attrs={'placeholder': 'Ej: 18,000 BTU'}),
            'TipoGasRefrigerante': forms.TextInput(attrs={'placeholder': 'Ej: R-410A'}),
            'ServicioRealizado': forms.TextInput(attrs={'placeholder': 'Mantenimiento preventivo'}),
        }