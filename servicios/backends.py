from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib import messages # <-- 1. IMPORTACIÓN NECESARIA PARA MENSAJES
from .models import Usuarios

class EmailBackend(BaseBackend):
    """
    Autentica al usuario buscando por el campo CorreoElectronico en 
    el modelo Usuarios (tu tabla de DB).
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = Usuarios 
        
        try:
            # 1. Busca al usuario usando el correo electrónico.
            # Se usa 'CorreoElectronico' (C y E mayúsculas) para coincidir con el modelo.
            user = UserModel.objects.get(CorreoElectronico=username) 
            
        except UserModel.DoesNotExist:
            # 2. MENSAJE DE ERROR ESPECÍFICO: USUARIO NO ENCONTRADO
            messages.error(request, 'El correo electrónico o nombre de usuario no existe.')
            return None # Retorna None si el usuario no existe

        # 3. Verifica la contraseña hasheada
        if check_password(password, user.password):
            return user # Contraseña válida, retorna el objeto usuario
        
        # 4. MENSAJE DE ERROR ESPECÍFICO: CONTRASEÑA INCORRECTA
        messages.error(request, 'Contraseña incorrecta. Inténtalo de nuevo.')
        return None # Retorna None si la contraseña es inválida

    def get_user(self, user_id):
        """
        Método requerido para que Django pueda recuperar el objeto usuario 
        a partir de su ID después de iniciar sesión.
        """
        UserModel = Usuarios
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None