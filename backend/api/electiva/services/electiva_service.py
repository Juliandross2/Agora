from typing import List, Dict, Any, Optional, Tuple
from api.electiva.repositories.electiva_repository import ElectivaRepository
from api.electiva.serializers.electiva_serializer import ElectivaSerializer, ElectivaCreateSerializer, ElectivaUpdateSerializer
from api.electiva.models.electiva import Electiva

class ElectivaService:
    """Service para manejar la lógica de negocio de Electiva"""
    
    def __init__(self):
        self.repository = ElectivaRepository()
    
    def obtener_todas_electivas(self) -> Tuple[bool, Dict[str, Any]]:
        """Obtener todas las electivas"""
        try:
            electivas = self.repository.obtener_todas()
            
            if not electivas:
                return True, {
                    'message': 'No hay electivas registradas',
                    'electivas': [],
                    'total': 0
                }
            
            serializer = ElectivaSerializer(electivas, many=True)
            return True, {
                'message': 'Electivas obtenidas exitosamente',
                'electivas': serializer.data,
                'total': len(electivas)
            }
        except Exception as e:
            print(f"[SERVICE] Error al obtener electivas: {e}")
            return False, {
                'error': 'Error interno al obtener electivas',
                'details': str(e)
            }
    
    def obtener_electiva_por_id(self, electiva_id: int) -> Tuple[bool, Dict[str, Any]]:
        """Obtener electiva por ID"""
        try:
            if not electiva_id or electiva_id <= 0:
                return False, {
                    'error': 'ID de electiva inválido'
                }
            
            electiva = self.repository.obtener_por_id(electiva_id)
            
            if not electiva:
                return False, {
                    'error': 'Electiva no encontrada'
                }
            
            serializer = ElectivaSerializer(electiva)
            return True, {
                'message': 'Electiva obtenida exitosamente',
                'electiva': serializer.data
            }
        except Exception as e:
            print(f"[SERVICE] Error al obtener electiva {electiva_id}: {e}")
            return False, {
                'error': 'Error interno al obtener electiva',
                'details': str(e)
            }
    
    def crear_electiva(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Crear nueva electiva"""
        try:
            # Validar datos con serializer
            serializer = ElectivaCreateSerializer(data=data)
            if not serializer.is_valid():
                return False, {
                    'error': 'Datos inválidos',
                    'details': serializer.errors
                }
            
            # Crear electiva usando repository
            success, electiva, message = self.repository.crear(serializer.validated_data)
            
            if not success:
                return False, {
                    'error': message
                }
            
            # Serializar respuesta
            electiva_serializer = ElectivaSerializer(electiva)
            return True, {
                'message': message,
                'electiva': electiva_serializer.data
            }
        except Exception as e:
            print(f"[SERVICE] Error al crear electiva: {e}")
            return False, {
                'error': 'Error interno al crear electiva',
                'details': str(e)
            }
    
    def actualizar_electiva(self, electiva_id: int, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Actualizar electiva existente"""
        try:
            if not electiva_id or electiva_id <= 0:
                return False, {
                    'error': 'ID de electiva inválido'
                }
            
            # Validar datos con serializer
            serializer = ElectivaUpdateSerializer(data=data)
            if not serializer.is_valid():
                return False, {
                    'error': 'Datos inválidos',
                    'details': serializer.errors
                }
            
            # Verificar que la electiva existe
            electiva_existente = self.repository.obtener_por_id(electiva_id)
            if not electiva_existente:
                return False, {
                    'error': 'Electiva no encontrada'
                }
            
            # Actualizar electiva usando repository
            success, electiva, message = self.repository.actualizar(electiva_id, serializer.validated_data)
            
            if not success:
                return False, {
                    'error': message
                }
            
            # Serializar respuesta
            electiva_serializer = ElectivaSerializer(electiva)
            return True, {
                'message': message,
                'electiva': electiva_serializer.data
            }
        except Exception as e:
            print(f"[SERVICE] Error al actualizar electiva {electiva_id}: {e}")
            return False, {
                'error': 'Error interno al actualizar electiva',
                'details': str(e)
            }
    
    def eliminar_electiva(self, electiva_id: int) -> Tuple[bool, Dict[str, Any]]:
        """Eliminar electiva"""
        try:
            if not electiva_id or electiva_id <= 0:
                return False, {
                    'error': 'ID de electiva inválido'
                }
            
            # Verificar que la electiva existe
            electiva = self.repository.obtener_por_id(electiva_id)
            if not electiva:
                return False, {
                    'error': 'Electiva no encontrada'
                }
            
            # Eliminar electiva usando repository
            success, message = self.repository.eliminar(electiva_id)
            
            if not success:
                return False, {
                    'error': message
                }
            
            return True, {
                'message': message
            }
        except Exception as e:
            print(f"[SERVICE] Error al eliminar electiva {electiva_id}: {e}")
            return False, {
                'error': 'Error interno al eliminar electiva',
                'details': str(e)
            }
    
    def obtener_electivas_activas(self) -> Tuple[bool, Dict[str, Any]]:
        """Obtener solo electivas activas"""
        try:
            electivas = self.repository.obtener_activas()
            
            if not electivas:
                return True, {
                    'message': 'No hay electivas activas',
                    'electivas': [],
                    'total': 0
                }
            
            serializer = ElectivaSerializer(electivas, many=True)
            return True, {
                'message': 'Electivas activas obtenidas exitosamente',
                'electivas': serializer.data,
                'total': len(electivas)
            }
        except Exception as e:
            print(f"[SERVICE] Error al obtener electivas activas: {e}")
            return False, {
                'error': 'Error interno al obtener electivas activas',
                'details': str(e)
            }
    
    def obtener_electivas_por_programa(self, programa_id: int) -> Tuple[bool, Dict[str, Any]]:
        """Obtener electivas por programa"""
        try:
            if not programa_id or programa_id <= 0:
                return False, {
                    'error': 'ID de programa inválido'
                }
            
            electivas = self.repository.obtener_por_programa(programa_id)
            
            if not electivas:
                return True, {
                    'message': f'No hay electivas para el programa {programa_id}',
                    'electivas': [],
                    'total': 0
                }
            
            serializer = ElectivaSerializer(electivas, many=True)
            return True, {
                'message': f'Electivas del programa {programa_id} obtenidas exitosamente',
                'electivas': serializer.data,
                'total': len(electivas)
            }
        except Exception as e:
            print(f"[SERVICE] Error al obtener electivas por programa {programa_id}: {e}")
            return False, {
                'error': 'Error interno al obtener electivas por programa',
                'details': str(e)
            }
    
    def buscar_electivas_por_nombre(self, nombre: str) -> Tuple[bool, Dict[str, Any]]:
        """Buscar electivas por nombre"""
        try:
            if not nombre or not nombre.strip():
                return False, {
                    'error': 'Nombre de búsqueda requerido'
                }
            
            electivas = self.repository.buscar_por_nombre(nombre.strip())
            
            if not electivas:
                return True, {
                    'message': f'No se encontraron electivas con el nombre "{nombre}"',
                    'electivas': [],
                    'total': 0
                }
            
            serializer = ElectivaSerializer(electivas, many=True)
            return True, {
                'message': f'Electivas encontradas para "{nombre}"',
                'electivas': serializer.data,
                'total': len(electivas)
            }
        except Exception as e:
            print(f"[SERVICE] Error al buscar electivas por nombre '{nombre}': {e}")
            return False, {
                'error': 'Error interno al buscar electivas',
                'details': str(e)
            }

