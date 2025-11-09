import pandas as pd
import unicodedata
from ..config.config import CONFIG


def _normalize_text(s):
    """Normaliza textos: elimina acentos, convierte a minúsculas y hace strip."""
    if pd.isna(s):
        return ""
    s = str(s)
    s = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('utf-8')
    return s.strip().lower()


def comparar_estudiante(historia, pensum):
    semestre_limite = CONFIG["semestre_limite_electivas"]
    nota_aprobatoria = CONFIG["nota_aprobatoria"]

    # Normalizar columnas y valores de materia en pensum
    pensum.columns = pensum.columns.str.strip().str.lower()
    if 'materia' in pensum.columns:
        pensum['materia'] = pensum['materia'].apply(_normalize_text)

    # Pensum hasta semestre límite
    pensum_limite = pensum[pensum["semestre"] <= semestre_limite]
    materias_requeridas = pensum_limite["materia"].tolist()

    # Normalizar valores de materia en historia
    historia.columns = historia.columns.str.strip().str.lower()
    if 'materia' in historia.columns:
        historia['materia'] = historia['materia'].apply(_normalize_text)

    # Materias aprobadas: si en cualquier semestre la materia tiene definitiva >= nota_aprobatoria
    aprobadas = historia.loc[historia["definitiva"] >= nota_aprobatoria, "materia"].unique().tolist()

    # Semestre máximo cursado (asegurar entero)
    try:
        semestre_max = int(pd.to_numeric(historia["semestre"], errors='coerce').max())
    except Exception:
        semestre_max = 0

    # Créditos aprobados: sumar créditos del pensum para materias aprobadas (evita doble conteo por reintentos)
    if 'créditos' in pensum.columns:
        creditos_aprobados = pensum[pensum['materia'].isin(aprobadas)]['créditos'].sum()
    else:
        # Fallback: sumar créditos desde la historia (si existen)
        creditos_aprobados = historia.loc[historia["definitiva"] >= nota_aprobatoria, "créditos"].sum()

    # Periodos matriculados
    periodos_matriculados = historia["periodo"].nunique() if 'periodo' in historia.columns else 0

    # Verificación de "nivelado"
    nivelado = False
    if semestre_max in CONFIG.get("niveles_creditos_periodos", {}):
        regla = CONFIG["niveles_creditos_periodos"][semestre_max]
        if creditos_aprobados >= regla["min_creditos"] and periodos_matriculados <= regla["max_periodos"]:
            nivelado = True

    # Porcentaje de avance
    porcentaje_avance = creditos_aprobados / CONFIG["total_creditos_obligatorios"] if CONFIG.get("total_creditos_obligatorios") else 0

    # Materias que faltan hasta el semestre límite (comparando nombres normalizados)
    faltantes = [m for m in materias_requeridas if m not in aprobadas]

    # Elegibilidad
    if nivelado and not faltantes:
        estado = 1
    elif porcentaje_avance >= CONFIG.get("porcentaje_avance_minimo", 0) and semestre_max >= semestre_limite and not faltantes:
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
