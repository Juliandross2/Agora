import pandas as pd
from ..config.config import CONFIG

def comparar_estudiante(historia, pensum):
    semestre_limite = CONFIG["semestre_limite_electivas"]
    nota_aprobatoria = CONFIG["nota_aprobatoria"]

    # Pensum hasta semestre límite
    pensum.columns = pensum.columns.str.strip().str.lower()
    pensum_limite = pensum[pensum["semestre"] <= semestre_limite]
    materias_requeridas = pensum_limite["materia"].str.strip().str.lower().tolist()

    # Materias aprobadas
    aprobadas = historia[historia["definitiva"] >= nota_aprobatoria]["materia"].unique().tolist()

    # Semestre máximo cursado
    semestre_max = int(historia["semestre"].max())

    # Créditos aprobados
    creditos_aprobados = historia[historia["definitiva"] >= nota_aprobatoria]["créditos"].sum()

    # Periodos matriculados
    periodos_matriculados = historia["periodo"].nunique()

    # Verificación de "nivelado"
    nivelado = False
    if semestre_max in CONFIG["niveles_creditos_periodos"]:
        regla = CONFIG["niveles_creditos_periodos"][semestre_max]
        if creditos_aprobados >= regla["min_creditos"] and periodos_matriculados <= regla["max_periodos"]:
            nivelado = True

    # Porcentaje de avance
    porcentaje_avance = creditos_aprobados / CONFIG["total_creditos_obligatorios"]

    faltantes = [m for m in materias_requeridas if m not in aprobadas]

    # Elegibilidad
    if nivelado and not faltantes:
        estado = 1
    elif porcentaje_avance >= CONFIG["porcentaje_avance_minimo"] and semestre_max >= semestre_limite and not faltantes:
        estado = 1
    else:
        estado = 0

    return {
        "semestre_maximo": semestre_max,
        "creditos_aprobados": int(creditos_aprobados),
        "periodos_matriculados": int(periodos_matriculados),
        "porcentaje_avance": round(porcentaje_avance * 100, 2),
        "nivelado": nivelado,
        "estado": estado,
        "materias_faltantes_hasta_semestre_limite": faltantes
    }
