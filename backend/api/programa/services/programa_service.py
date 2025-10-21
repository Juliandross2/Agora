from typing import List, Dict, Any, Optional, Tuple
from api.programa.repositories.programa_repository import ProgramaRepository
from api.programa.serializers.programa_serializer import ProgramaSerializer, ProgramaCreateSerializer, ProgramaUpdateSerializer
from api.programa.models.programa import Programa

class ProgramaService:
    """Service para manejar la lógica de negocio de Programa"""
    
    def __init__(self):
        self.repository = ProgramaRepository()
    
    def obtener_todos_programas(self) -> Tuple[bool, Dict[str, Any]]:
        """Obtener todos los programas"""
        try:
            programas = self.repository.obtener_todos()
            
            if not programas:
                return True, {
                    'message': 'No hay programas registrados',
                    'programas': [],
                    'total': 0
                }
            
            serializer = ProgramaSerializer(programas, many=True)
            return True, {
                'message': 'Programas obtenidos exitosamente',
                'programas': serializer.data,
                'total': len(programas)
            }
        except Exception as e:
            print(f"[SERVICE] Error al obtener programas: {e}")
            return False, {
                'error': 'Error interno al obtener programas',
                'details': str(e)
            }
    
    def obtener_programa_por_id(self, programa_id: int) -> Tuple[bool, Dict[str, Any]]:
        """Obtener programa por ID"""
        try:
            if not programa_id or programa_id <= 0:
                return False, {
                    'error': 'ID de programa inválido'
                }
            
            programa = self.repository.obtener_por_id(programa_id)
            
            if not programa:
                return False, {
                    'error': 'Programa no encontrado'
                }
            
            serializer = ProgramaSerializer(programa)
            return True, {
                'message': 'Programa obtenido exitosamente',
                'programa': serializer.data
            }
        except Exception as e:
            print(f"[SERVICE] Error al obtener programa {programa_id}: {e}")
            return False, {
                'error': 'Error interno al obtener programa',
                'details': str(e)
            }
    
    def crear_programa(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Crear nuevo programa"""
        try:
            # Validar datos con serializer
            serializer = ProgramaCreateSerializer(data=data)
            if not serializer.is_valid():
                return False, {
                    'error': 'Datos inválidos',
                    'details': serializer.errors
                }
            
            # Crear programa usando repository
            success, programa, message = self.repository.crear(serializer.validated_data)
            
            if not success:
                return False, {
                    'error': message
                }
            
            # Serializar respuesta
            programa_serializer = ProgramaSerializer(programa)
            return True, {
                'message': message,
                'programa': programa_serializer.data
            }
        except Exception as e:
            print(f"[SERVICE] Error al crear programa: {e}")
            return False, {
                'error': 'Error interno al crear programa',
                'details': str(e)
            }
    
    def actualizar_programa(self, programa_id: int, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Actualizar programa existente"""
        try:
            if not programa_id or programa_id <= 0:
                return False, {
                    'error': 'ID de programa inválido'
                }
            
            # Validar datos con serializer
            serializer = ProgramaUpdateSerializer(data=data)
            if not serializer.is_valid():
                return False, {
                    'error': 'Datos inválidos',
                    'details': serializer.errors
                }
            
            # Verificar que el programa existe
            programa_existente = self.repository.obtener_por_id(programa_id)
            if not programa_existente:
                return False, {
                    'error': 'Programa no encontrado'
                }
            
            # Actualizar programa usando repository
            success, programa, message = self.repository.actualizar(programa_id, serializer.validated_data)
            
            if not success:
                return False, {
                    'error': message
                }
            
            # Serializar respuesta
            programa_serializer = ProgramaSerializer(programa)
            return True, {
                'message': message,
                'programa': programa_serializer.data
            }
        except Exception as e:
            print(f"[SERVICE] Error al actualizar programa {programa_id}: {e}")
            return False, {
                'error': 'Error interno al actualizar programa',
                'details': str(e)
            }
    
    def eliminar_programa(self, programa_id: int) -> Tuple[bool, Dict[str, Any]]:
        """Eliminar programa"""
        try:
            if not programa_id or programa_id <= 0:
                return False, {
                    'error': 'ID de programa inválido'
                }
            
            # Verificar que el programa existe
            programa = self.repository.obtener_por_id(programa_id)
            if not programa:
                return False, {
                    'error': 'Programa no encontrado'
                }
            
            # Eliminar programa usando repository
            success, message = self.repository.eliminar(programa_id)
            
            if not success:
                return False, {
                    'error': message
                }
            
            return True, {
                'message': message
            }
        except Exception as e:
            print(f"[SERVICE] Error al eliminar programa {programa_id}: {e}")
            return False, {
                'error': 'Error interno al eliminar programa',
                'details': str(e)
            }
    
    def obtener_programas_activos(self) -> Tuple[bool, Dict[str, Any]]:
        """Obtener solo programas activos"""
        try:
            programas = self.repository.obtener_activos()
            
            if not programas:
                return True, {
                    'message': 'No hay programas activos',
                    'programas': [],
                    'total': 0
                }
            
            serializer = ProgramaSerializer(programas, many=True)
            return True, {
                'message': 'Programas activos obtenidos exitosamente',
                'programas': serializer.data,
                'total': len(programas)
            }
        except Exception as e:
            print(f"[SERVICE] Error al obtener programas activos: {e}")
            return False, {
                'error': 'Error interno al obtener programas activos',
                'details': str(e)
            }
    
    def buscar_programas_por_nombre(self, nombre: str) -> Tuple[bool, Dict[str, Any]]:
        """Buscar programas por nombre"""
        try:
            if not nombre or not nombre.strip():
                return False, {
                    'error': 'Nombre de búsqueda requerido'
                }
            
            programas = self.repository.buscar_por_nombre(nombre.strip())
            
            if not programas:
                return True, {
                    'message': f'No se encontraron programas con el nombre "{nombre}"',
                    'programas': [],
                    'total': 0
                }
            
            serializer = ProgramaSerializer(programas, many=True)
            return True, {
                'message': f'Programas encontrados para "{nombre}"',
                'programas': serializer.data,
                'total': len(programas)
            }
        except Exception as e:
            print(f"[SERVICE] Error al buscar programas por nombre '{nombre}': {e}")
            return False, {
                'error': 'Error interno al buscar programas',
                'details': str(e)
            }
