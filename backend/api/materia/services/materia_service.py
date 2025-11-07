from typing import List, Dict, Any, Optional, Tuple
from api.materia.repositories.materia_repository import MateriaRepository
from api.materia.serializers.materia_serializer import MateriaSerializer, MateriaCreateSerializer, MateriaUpdateSerializer
from api.materia.models.materia import Materia

class MateriaService:
    """Service para manejar la lógica de negocio de Materia"""
    
    def __init__(self):
        self.repository = MateriaRepository()
    
    def obtener_todas_materias(self) -> Tuple[bool, Dict[str, Any]]:
        """Obtener todas las materias"""
        try:
            materias = self.repository.obtener_todas()
            
            if not materias:
                return True, {
                    'message': 'No hay materias registradas',
                    'materias': [],
                    'total': 0
                }
            
            serializer = MateriaSerializer(materias, many=True)
            return True, {
                'message': 'Materias obtenidas exitosamente',
                'materias': serializer.data,
                'total': len(materias)
            }
        except Exception as e:
            print(f"[SERVICE] Error al obtener materias: {e}")
            return False, {
                'error': 'Error interno al obtener materias',
                'details': str(e)
            }
    
    def obtener_materia_por_id(self, materia_id: int) -> Tuple[bool, Dict[str, Any]]:
        """Obtener materia por ID"""
        try:
            if not materia_id or materia_id <= 0:
                return False, {
                    'error': 'ID de materia inválido'
                }
            
            materia = self.repository.obtener_por_id(materia_id)
            
            if not materia:
                return False, {
                    'error': 'Materia no encontrada'
                }
            
            serializer = MateriaSerializer(materia)
            return True, {
                'message': 'Materia obtenida exitosamente',
                'materia': serializer.data
            }
        except Exception as e:
            print(f"[SERVICE] Error al obtener materia {materia_id}: {e}")
            return False, {
                'error': 'Error interno al obtener materia',
                'details': str(e)
            }
    
    def crear_materia(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Crear nueva materia"""
        try:
            # Validar datos con serializer
            serializer = MateriaCreateSerializer(data=data)
            if not serializer.is_valid():
                return False, {
                    'error': 'Datos inválidos',
                    'details': serializer.errors
                }
            
            # Crear materia usando repository
            success, materia, message = self.repository.crear(serializer.validated_data)
            
            if not success:
                return False, {
                    'error': message
                }
            
            # Serializar respuesta
            materia_serializer = MateriaSerializer(materia)
            return True, {
                'message': message,
                'materia': materia_serializer.data
            }
        except Exception as e:
            print(f"[SERVICE] Error al crear materia: {e}")
            return False, {
                'error': 'Error interno al crear materia',
                'details': str(e)
            }
    
    def actualizar_materia(self, materia_id: int, data: Dict[str, Any], partial: bool = False) -> Tuple[bool, Dict[str, Any]]:
        """Actualizar materia existente"""
        try:
            if not materia_id or materia_id <= 0:
                return False, {
                    'error': 'ID de materia inválido'
                }
            
            # Validar datos con serializer
            # usar partial=True para patch (validación parcial)
            serializer = MateriaUpdateSerializer(data=data, partial=partial)
            if not serializer.is_valid():
                return False, {
                    'error': 'Datos inválidos',
                    'details': serializer.errors
                }
            
            # Verificar que la materia existe
            materia_existente = self.repository.obtener_por_id(materia_id)
            if not materia_existente:
                return False, {
                    'error': 'Materia no encontrada'
                }
            
            # Actualizar materia usando repository
            success, materia, message = self.repository.actualizar(materia_id, serializer.validated_data)
            
            if not success:
                return False, {
                    'error': message
                }
            
            # Serializar respuesta
            materia_serializer = MateriaSerializer(materia)
            return True, {
                'message': message,
                'materia': materia_serializer.data
            }
        except Exception as e:
            print(f"[SERVICE] Error al actualizar materia {materia_id}: {e}")
            return False, {
                'error': 'Error interno al actualizar materia',
                'details': str(e)
            }
    
    def eliminar_materia(self, materia_id: int) -> Tuple[bool, Dict[str, Any]]:
        """Eliminar materia"""
        try:
            if not materia_id or materia_id <= 0:
                return False, {
                    'error': 'ID de materia inválido'
                }
            
            # Verificar que la materia existe
            materia = self.repository.obtener_por_id(materia_id)
            if not materia:
                return False, {
                    'error': 'Materia no encontrada'
                }
            
            # Eliminar materia usando repository
            success, message = self.repository.eliminar(materia_id)
            
            if not success:
                return False, {
                    'error': message
                }
            
            return True, {
                'message': message
            }
        except Exception as e:
            print(f"[SERVICE] Error al eliminar materia {materia_id}: {e}")
            return False, {
                'error': 'Error interno al eliminar materia',
                'details': str(e)
            }
    
    def obtener_materias_activas(self) -> Tuple[bool, Dict[str, Any]]:
        """Obtener solo materias activas"""
        try:
            materias = self.repository.obtener_activas()
            
            if not materias:
                return True, {
                    'message': 'No hay materias activas',
                    'materias': [],
                    'total': 0
                }
            
            serializer = MateriaSerializer(materias, many=True)
            return True, {
                'message': 'Materias activas obtenidas exitosamente',
                'materias': serializer.data,
                'total': len(materias)
            }
        except Exception as e:
            print(f"[SERVICE] Error al obtener materias activas: {e}")
            return False, {
                'error': 'Error interno al obtener materias activas',
                'details': str(e)
            }
    
    def obtener_materias_por_pensum(self, pensum_id: int) -> Tuple[bool, Dict[str, Any]]:
        """Obtener materias por pensum"""
        try:
            if not pensum_id or pensum_id <= 0:
                return False, {
                    'error': 'ID de pensum inválido'
                }
            
            materias = self.repository.obtener_por_pensum(pensum_id)
            
            if not materias:
                return True, {
                    'message': f'No hay materias para el pensum {pensum_id}',
                    'materias': [],
                    'total': 0
                }
            
            serializer = MateriaSerializer(materias, many=True)
            return True, {
                'message': f'Materias del pensum {pensum_id} obtenidas exitosamente',
                'materias': serializer.data,
                'total': len(materias)
            }
        except Exception as e:
            print(f"[SERVICE] Error al obtener materias por pensum {pensum_id}: {e}")
            return False, {
                'error': 'Error interno al obtener materias por pensum',
                'details': str(e)
            }
    
    def obtener_materias_por_semestre(self, semestre: int) -> Tuple[bool, Dict[str, Any]]:
        """Obtener materias por semestre"""
        try:
            if not semestre or semestre <= 0:
                return False, {
                    'error': 'Semestre inválido'
                }
            
            materias = self.repository.obtener_por_semestre(semestre)
            
            if not materias:
                return True, {
                    'message': f'No hay materias en el semestre {semestre}',
                    'materias': [],
                    'total': 0
                }
            
            serializer = MateriaSerializer(materias, many=True)
            return True, {
                'message': f'Materias del semestre {semestre} obtenidas exitosamente',
                'materias': serializer.data,
                'total': len(materias)
            }
        except Exception as e:
            print(f"[SERVICE] Error al obtener materias por semestre {semestre}: {e}")
            return False, {
                'error': 'Error interno al obtener materias por semestre',
                'details': str(e)
            }
    
    def buscar_materias_por_nombre(self, nombre: str) -> Tuple[bool, Dict[str, Any]]:
        """Buscar materias por nombre"""
        try:
            if not nombre or not nombre.strip():
                return False, {
                    'error': 'Nombre de búsqueda requerido'
                }
            
            materias = self.repository.buscar_por_nombre(nombre.strip())
            
            if not materias:
                return True, {
                    'message': f'No se encontraron materias con el nombre "{nombre}"',
                    'materias': [],
                    'total': 0
                }
            
            serializer = MateriaSerializer(materias, many=True)
            return True, {
                'message': f'Materias encontradas para "{nombre}"',
                'materias': serializer.data,
                'total': len(materias)
            }
        except Exception as e:
            print(f"[SERVICE] Error al buscar materias por nombre '{nombre}': {e}")
            return False, {
                'error': 'Error interno al buscar materias',
                'details': str(e)
            }
    
    def obtener_materias_obligatorias(self) -> Tuple[bool, Dict[str, Any]]:
        """Obtener solo materias obligatorias"""
        try:
            materias = self.repository.obtener_obligatorias()
            
            if not materias:
                return True, {
                    'message': 'No hay materias obligatorias',
                    'materias': [],
                    'total': 0
                }
            
            serializer = MateriaSerializer(materias, many=True)
            return True, {
                'message': 'Materias obligatorias obtenidas exitosamente',
                'materias': serializer.data,
                'total': len(materias)
            }
        except Exception as e:
            print(f"[SERVICE] Error al obtener materias obligatorias: {e}")
            return False, {
                'error': 'Error interno al obtener materias obligatorias',
                'details': str(e)
            }


