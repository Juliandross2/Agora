from django.db import models
from api.programa.models.programa import Programa
from typing import List, Dict, Any, Optional, Tuple

class ProgramaRepository:
    """Repository para manejar el acceso a datos de Programa"""
    
    def obtener_todos(self) -> List[Programa]:
        """Obtener todos los programas"""
        try:
            return list(Programa.objects.all())
        except Exception as e:
            print(f"[REPOSITORY] Error al obtener programas: {e}")
            return []
    
    def obtener_por_id(self, programa_id: int) -> Optional[Programa]:
        """Obtener programa por ID"""
        try:
            return Programa.objects.get(programa_id=programa_id)
        except Programa.DoesNotExist:
            return None
        except Exception as e:
            print(f"[REPOSITORY] Error al obtener programa por ID {programa_id}: {e}")
            return None
    
    def crear(self, data: Dict[str, Any]) -> Tuple[bool, Optional[Programa], str]:
        """Crear nuevo programa"""
        try:
            programa = Programa.objects.create(
                nombre_programa=data['nombre_programa'],
                es_activo=data.get('es_activo', True)
            )
            return True, programa, "Programa creado exitosamente"
        except Exception as e:
            print(f"[REPOSITORY] Error al crear programa: {e}")
            return False, None, f"Error al crear programa: {str(e)}"
    
    def actualizar(self, programa_id: int, data: Dict[str, Any]) -> Tuple[bool, Optional[Programa], str]:
        """Actualizar programa existente"""
        try:
            programa = Programa.objects.get(programa_id=programa_id)
            
            if 'nombre_programa' in data:
                programa.nombre_programa = data['nombre_programa']
            if 'es_activo' in data:
                programa.es_activo = data['es_activo']
            
            programa.save()
            return True, programa, "Programa actualizado exitosamente"
        except Programa.DoesNotExist:
            return False, None, "Programa no encontrado"
        except Exception as e:
            print(f"[REPOSITORY] Error al actualizar programa {programa_id}: {e}")
            return False, None, f"Error al actualizar programa: {str(e)}"
    
    def eliminar(self, programa_id: int) -> Tuple[bool, str]:
        """Eliminar programa (soft delete - actualiza es_activo a False)"""
        try:
            programa = Programa.objects.get(programa_id=programa_id)
            programa.es_activo = False
            programa.save()
            return True, "Programa marcado como inactivo exitosamente"
        except Programa.DoesNotExist:
            return False, "Programa no encontrado"
        except Exception as e:
            print(f"[REPOSITORY] Error al eliminar programa {programa_id}: {e}")
            return False, f"Error al eliminar programa: {str(e)}"
    
    def obtener_activos(self) -> List[Programa]:
        """Obtener solo programas activos"""
        try:
            return list(Programa.objects.filter(es_activo=True))
        except Exception as e:
            print(f"[REPOSITORY] Error al obtener programas activos: {e}")
            return []
    
    def buscar_por_nombre(self, nombre: str) -> List[Programa]:
        """Buscar programas por nombre (búsqueda parcial)"""
        try:
            return list(Programa.objects.filter(nombre_programa__icontains=nombre))
        except Exception as e:
            print(f"[REPOSITORY] Error al buscar programas por nombre '{nombre}': {e}")
            return []
