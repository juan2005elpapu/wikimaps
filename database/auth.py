import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))
from usuarios import verificar_usuario, registrar_usuario, usuario_existe, email_existe

class UserAuth:
    @staticmethod
    def login(username, password):
        """
        Verifica las credenciales del usuario para el inicio de sesión.
        """
        return verificar_usuario(username, password)
    
    @staticmethod
    def register(username, password, email):
        """
        Registra un nuevo usuario en el sistema.
        """
        # Validaciones básicas
        if not username or not password or not email:
            return False, "Todos los campos son obligatorios"
        
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
        
        if "@" not in email or "." not in email:
            return False, "El formato del correo electrónico no es válido"
        
        # Verificar si el usuario ya existe
        existe, _ = usuario_existe(username)
        if existe:
            return False, "El nombre de usuario ya está en uso"
        
        # Verificar si el email ya existe
        existe, _ = email_existe(email)
        if existe:
            return False, "El correo electrónico ya está registrado"
        
        # Registrar el usuario
        return registrar_usuario(username, password, email)