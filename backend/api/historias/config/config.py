# historias/config.py
"""
Valores por defecto para crear configuraciones de elegibilidad.
NOTA: Este CONFIG ya NO se usa como fallback, solo como valores por defecto
al crear nuevas configuraciones en la BD.
"""

CONFIG = {
    "nota_aprobatoria": 3.0,            # definitiva >= 3
    "semestre_limite_electivas": 7,     # Hasta qué semestre se exige tener TODO aprobado
}
