from django.contrib.auth.hashers import check_password
from api.usuario.models.usuario import Usuario
from typing import Optional

class UsuarioRepository:
    """Repositorio para manejar operaciones de base de datos del Usuario"""
    
    @staticmethod
    def crear_usuario(data: dict) -> Usuario:
        """Crear un nuevo usuario"""
        return Usuario.objects.create(**data)
    
    @staticmethod
    def obtener_por_email(email: str) -> Optional[Usuario]:
        """Obtener usuario por email"""
        try:
            return Usuario.objects.get(email_usuario=email, es_activo=True)
        except Usuario.DoesNotExist:
            return None
    
    @staticmethod
    def obtener_por_id(usuario_id: int) -> Optional[Usuario]:
        """Obtener usuario por ID"""
        try:
            return Usuario.objects.get(usuario_id=usuario_id, es_activo=True)
        except Usuario.DoesNotExist:
            return None
    
    @staticmethod
    def existe_email(email: str) -> bool:
        """Verificar si existe un email"""
        return Usuario.objects.filter(email_usuario=email).exists()
    
    @staticmethod
    def existe_nombre_usuario(nombre_usuario: str) -> bool:
        """Verificar si existe un nombre de usuario"""
        return Usuario.objects.filter(nombre_usuario=nombre_usuario).exists()
    
    @staticmethod
    def verificar_contrasenia(usuario: Usuario, contrasenia: str) -> bool:
        """Verificar si la contraseña es correcta"""
        return check_password(contrasenia, usuario.contrasenia)
    
    @staticmethod
    def actualizar_usuario(usuario: Usuario, data: dict) -> Usuario:
        """Actualizar datos del usuario"""
        for key, value in data.items():
            setattr(usuario, key, value)
        usuario.save()
        return usuario
    
    @staticmethod
    def desactivar_usuario(usuario: Usuario) -> Usuario:
        """Desactivar usuario en lugar de eliminarlo"""
        usuario.es_activo = False
        usuario.save()
        return usuario