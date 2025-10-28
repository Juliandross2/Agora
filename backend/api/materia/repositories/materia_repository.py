from django.db import models
from api.materia.models.materia import Materia
from typing import List, Dict, Any, Optional, Tuple

class MateriaRepository:
    """Repository para manejar el acceso a datos de Materia"""
    
    def obtener_todas(self) -> List[Materia]:
        """Obtener todas las materias"""
        try:
            return list(Materia.objects.select_related('pensum_id').all())
        except Exception as e:
            print(f"[REPOSITORY] Error al obtener materias: {e}")
            return []
    
    def obtener_por_id(self, materia_id: int) -> Optional[Materia]:
        """Obtener materia por ID"""
        try:
            return Materia.objects.select_related('pensum_id').get(materia_id=materia_id)
        except Materia.DoesNotExist:
            return None
        except Exception as e:
            print(f"[REPOSITORY] Error al obtener materia por ID {materia_id}: {e}")
            return None
    
    def crear(self, data: Dict[str, Any]) -> Tuple[bool, Optional[Materia], str]:
        """Crear nueva materia"""
        try:
            from api.pensum.models.pensum import Pensum
            
            # Obtener el pensum
            try:
                pensum = Pensum.objects.get(pensum_id=data['pensum_id'])
            except Pensum.DoesNotExist:
                return False, None, "El pensum especificado no existe"
            
            materia = Materia.objects.create(
                pensum_id=pensum,
                nombre_materia=data['nombre_materia'],
                creditos=data['creditos'],
                es_obligatoria=data.get('es_obligatoria', True),
                es_activa=data.get('es_activa', True),
                semestre=data['semestre']
            )
            return True, materia, "Materia creada exitosamente"
        except Exception as e:
            print(f"[REPOSITORY] Error al crear materia: {e}")
            return False, None, f"Error al crear materia: {str(e)}"
    
    def actualizar(self, materia_id: int, data: Dict[str, Any]) -> Tuple[bool, Optional[Materia], str]:
        """Actualizar materia existente"""
        try:
            materia = Materia.objects.get(materia_id=materia_id)
            
            if 'pensum_id' in data:
                from api.pensum.models.pensum import Pensum
                try:
                    pensum = Pensum.objects.get(pensum_id=data['pensum_id'])
                    materia.pensum_id = pensum
                except Pensum.DoesNotExist:
                    return False, None, "El pensum especificado no existe"
            
            if 'nombre_materia' in data:
                materia.nombre_materia = data['nombre_materia']
            if 'creditos' in data:
                materia.creditos = data['creditos']
            if 'es_obligatoria' in data:
                materia.es_obligatoria = data['es_obligatoria']
            if 'es_activa' in data:
                materia.es_activa = data['es_activa']
            if 'semestre' in data:
                materia.semestre = data['semestre']
            
            materia.save()
            return True, materia, "Materia actualizada exitosamente"
        except Materia.DoesNotExist:
            return False, None, "Materia no encontrada"
        except Exception as e:
            print(f"[REPOSITORY] Error al actualizar materia {materia_id}: {e}")
            return False, None, f"Error al actualizar materia: {str(e)}"
    
    def eliminar(self, materia_id: int) -> Tuple[bool, str]:
        """Eliminar materia (soft delete - actualiza es_activa a False)"""
        try:
            materia = Materia.objects.get(materia_id=materia_id)
            materia.es_activa = False
            materia.save()
            return True, "Materia marcada como inactiva exitosamente"
        except Materia.DoesNotExist:
            return False, "Materia no encontrada"
        except Exception as e:
            print(f"[REPOSITORY] Error al eliminar materia {materia_id}: {e}")
            return False, f"Error al eliminar materia: {str(e)}"
    
    def obtener_activas(self) -> List[Materia]:
        """Obtener solo materias activas"""
        try:
            return list(Materia.objects.select_related('pensum_id').filter(es_activa=True))
        except Exception as e:
            print(f"[REPOSITORY] Error al obtener materias activas: {e}")
            return []
    
    def obtener_por_pensum(self, pensum_id: int) -> List[Materia]:
        """Obtener materias por pensum"""
        try:
            return list(Materia.objects.filter(pensum_id=pensum_id))
        except Exception as e:
            print(f"[REPOSITORY] Error al obtener materias por pensum {pensum_id}: {e}")
            return []
    
    def obtener_por_semestre(self, semestre: int) -> List[Materia]:
        """Obtener materias por semestre"""
        try:
            return list(Materia.objects.select_related('pensum_id').filter(semestre=semestre))
        except Exception as e:
            print(f"[REPOSITORY] Error al obtener materias por semestre {semestre}: {e}")
            return []
    
    def buscar_por_nombre(self, nombre: str) -> List[Materia]:
        """Buscar materias por nombre (búsqueda parcial)"""
        try:
            return list(Materia.objects.select_related('pensum_id').filter(nombre_materia__icontains=nombre))
        except Exception as e:
            print(f"[REPOSITORY] Error al buscar materias por nombre '{nombre}': {e}")
            return []
    
    def obtener_obligatorias(self) -> List[Materia]:
        """Obtener solo materias obligatorias"""
        try:
            return list(Materia.objects.select_related('pensum_id').filter(es_obligatoria=True, es_activa=True))
        except Exception as e:
            print(f"[REPOSITORY] Error al obtener materias obligatorias: {e}")
            return []
    

