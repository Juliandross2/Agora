from django.db import models
from api.electiva.models.electiva import Electiva
from typing import List, Dict, Any, Optional, Tuple

class ElectivaRepository:
    """Repository para manejar el acceso a datos de Electiva"""
    
    def obtener_todas(self) -> List[Electiva]:
        """Obtener todas las electivas"""
        try:
            return list(Electiva.objects.select_related('programa_id').all())
        except Exception as e:
            print(f"[REPOSITORY] Error al obtener electivas: {e}")
            return []
    
    def obtener_por_id(self, electiva_id: int) -> Optional[Electiva]:
        """Obtener electiva por ID"""
        try:
            return Electiva.objects.select_related('programa_id').get(electiva_id=electiva_id)
        except Electiva.DoesNotExist:
            return None
        except Exception as e:
            print(f"[REPOSITORY] Error al obtener electiva por ID {electiva_id}: {e}")
            return None
    
    def crear(self, data: Dict[str, Any]) -> Tuple[bool, Optional[Electiva], str]:
        """Crear nueva electiva"""
        try:
            from api.programa.models.programa import Programa
            
            # Obtener el programa
            try:
                programa = Programa.objects.get(programa_id=data['programa_id'])
            except Programa.DoesNotExist:
                return False, None, "El programa especificado no existe"
            
            electiva = Electiva.objects.create(
                programa_id=programa,
                nombre_electiva=data['nombre_electiva'],
                descripcion=data.get('descripcion', None),
                es_activa=data.get('es_activa', True)
            )
            return True, electiva, "Electiva creada exitosamente"
        except Exception as e:
            print(f"[REPOSITORY] Error al crear electiva: {e}")
            return False, None, f"Error al crear electiva: {str(e)}"
    
    def actualizar(self, electiva_id: int, data: Dict[str, Any]) -> Tuple[bool, Optional[Electiva], str]:
        """Actualizar electiva existente"""
        try:
            electiva = Electiva.objects.get(electiva_id=electiva_id)
            
            if 'programa_id' in data:
                from api.programa.models.programa import Programa
                try:
                    programa = Programa.objects.get(programa_id=data['programa_id'])
                    electiva.programa_id = programa
                except Programa.DoesNotExist:
                    return False, None, "El programa especificado no existe"
            
            if 'nombre_electiva' in data:
                electiva.nombre_electiva = data['nombre_electiva']
            if 'descripcion' in data:
                electiva.descripcion = data.get('descripcion')
            if 'es_activa' in data:
                electiva.es_activa = data['es_activa']
            
            electiva.save()
            return True, electiva, "Electiva actualizada exitosamente"
        except Electiva.DoesNotExist:
            return False, None, "Electiva no encontrada"
        except Exception as e:
            print(f"[REPOSITORY] Error al actualizar electiva {electiva_id}: {e}")
            return False, None, f"Error al actualizar electiva: {str(e)}"
    
    def eliminar(self, electiva_id: int) -> Tuple[bool, str]:
        """Eliminar electiva (soft delete - actualiza es_activa a False)"""
        try:
            electiva = Electiva.objects.get(electiva_id=electiva_id)
            electiva.es_activa = False
            electiva.save()
            return True, "Electiva marcada como inactiva exitosamente"
        except Electiva.DoesNotExist:
            return False, "Electiva no encontrada"
        except Exception as e:
            print(f"[REPOSITORY] Error al eliminar electiva {electiva_id}: {e}")
            return False, f"Error al eliminar electiva: {str(e)}"
    
    def obtener_activas(self) -> List[Electiva]:
        """Obtener solo electivas activas"""
        try:
            return list(Electiva.objects.select_related('programa_id').filter(es_activa=True))
        except Exception as e:
            print(f"[REPOSITORY] Error al obtener electivas activas: {e}")
            return []
    
    def obtener_por_programa(self, programa_id: int) -> List[Electiva]:
        """Obtener electivas por programa"""
        try:
            return list(Electiva.objects.filter(programa_id=programa_id))
        except Exception as e:
            print(f"[REPOSITORY] Error al obtener electivas por programa {programa_id}: {e}")
            return []
    
    def buscar_por_nombre(self, nombre: str) -> List[Electiva]:
        """Buscar electivas por nombre (búsqueda parcial)"""
        try:
            return list(Electiva.objects.select_related('programa_id').filter(nombre_electiva__icontains=nombre))
        except Exception as e:
            print(f"[REPOSITORY] Error al buscar electivas por nombre '{nombre}': {e}")
            return []

