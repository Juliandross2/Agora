# historias/config.py
"""
Valores por defecto para crear configuraciones de elegibilidad.
NOTA: Este CONFIG ya NO se usa como fallback, solo como valores por defecto
al crear nuevas configuraciones en la BD.
"""

CONFIG = {
    "porcentaje_avance_minimo": 0.60,   # 60%
    "nota_aprobatoria": 3.0,            # definitiva >= 3
    "semestre_limite_electivas": 7,     # Hasta qué semestre se exige tener TODO aprobado

    # Reglas según el protocolo para Sistemas
    "niveles_creditos_periodos": {
        8: {"min_creditos": 112, "max_periodos": 7},
        9: {"min_creditos": 132, "max_periodos": 8},
        10: {"min_creditos": 151, "max_periodos": 9}
    }
}
