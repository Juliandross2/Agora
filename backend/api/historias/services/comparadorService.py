import pandas as pd
import unicodedata
import re
from ..config.config import CONFIG


def obtener_pensum_desde_bd(programa_id):
    """
    Obtiene el pensum activo de un programa desde la base de datos y lo convierte a DataFrame.
    
    Args:
        programa_id: ID del programa académico
    
    Returns:
        DataFrame con columnas: materia, semestre, créditos
    
    Raises:
        ValueError: Si el programa no existe o no tiene pensum activo
    """
    from api.pensum.repositories.repository_pensum import PensumRepository
    from api.programa.models.programa import Programa
    
    # Validar que el programa existe
    try:
        programa = Programa.objects.get(pk=programa_id)
    except Programa.DoesNotExist:
        raise ValueError(f'Programa con ID {programa_id} no encontrado')
    
    # Obtener el pensum activo del programa
    repo = PensumRepository()
    pensum_obj = repo.get_current_by_programa(programa_id)
    
    if not pensum_obj:
        raise ValueError(f'No hay pensum activo para el programa "{programa.nombre_programa}" (ID: {programa_id})')
    
    # Obtener todas las materias activas del pensum
    materias = pensum_obj.materia_set.filter(es_activa=True).values('nombre_materia', 'semestre', 'creditos')
    
    if not materias.exists():
        raise ValueError(f'El pensum del programa "{programa.nombre_programa}" no tiene materias activas')
    
    # Convertir a DataFrame
    df = pd.DataFrame(list(materias))
    
    # Renombrar columnas para que coincidan con el formato esperado
    df.rename(columns={
        'nombre_materia': 'materia',
        'creditos': 'créditos'
    }, inplace=True)
    
    # Normalizar columnas
    df.columns = df.columns.str.strip().str.lower()
    
    return df


def _normalize_text(s):
    """Normaliza textos: elimina acentos, convierte a minúsculas y hace strip."""
    if pd.isna(s):
        return ""
    s = str(s)
    s = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('utf-8')
    return s.strip().lower()


def _es_fish(materia_nombre):
    """
    Verifica si una materia es una FISH (comienza con 'fish' seguido de espacio y número).
    
    Args:
        materia_nombre: Nombre normalizado de la materia
    
    Returns:
        True si es una FISH, False en caso contrario
    """
    patron = r'^fish\s*\d+$'
    return bool(re.match(patron, materia_nombre.strip()))


def _es_electiva_fish(materia_nombre):
    """
    Verifica si una materia es una Electiva Fish (comienza con 'electiva fish').
    
    Args:
        materia_nombre: Nombre normalizado de la materia
    
    Returns:
        True si es una Electiva Fish, False en caso contrario
    """
    return materia_nombre.strip().startswith('electiva fish')


def comparar_estudiante(historia, pensum, config=None, programa_id=None):
    """
    Compara la historia académica de un estudiante con el pensum para determinar elegibilidad.
    
    Args:
        historia: DataFrame con la historia académica del estudiante
        pensum: DataFrame con el pensum académico
        config: Diccionario opcional con configuración personalizada. Si es None, usa CONFIG por defecto.
                Debe contener: porcentaje_avance_minimo, nota_aprobatoria, semestre_limite_electivas,
                niveles_creditos_periodos
        programa_id: ID del programa para obtener el total de créditos del pensum
    
    Returns:
        Diccionario con los resultados de la comparación
    """
    # Validar que se proporcione configuración
    if config is None:
        raise ValueError("La configuración es requerida. Debe existir en la base de datos.")
    
    semestre_limite = config.get("semestre_limite_electivas")
    nota_aprobatoria = config.get("nota_aprobatoria")
    
    if semestre_limite is None or nota_aprobatoria is None:
        raise ValueError("La configuración está incompleta. Faltan campos requeridos.")

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

    # MANEJO ESPECIAL DE FISH: Contar cuántas Electivas Fish ha aprobado el estudiante
    electivas_fish_aprobadas = [m for m in aprobadas if _es_electiva_fish(m)]
    num_electivas_fish = len(electivas_fish_aprobadas)
    
    # Identificar las FISH en el pensum y marcarlas como aprobadas según las electivas fish del estudiante
    fish_en_pensum = []
    for materia in materias_requeridas:
        if _es_fish(materia):
            fish_en_pensum.append(materia)
    
    # Ordenar las FISH por número (fish 1, fish 2, fish 3, etc.)
    fish_en_pensum_ordenadas = sorted(fish_en_pensum, key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0)
    
    # Marcar como aprobadas las primeras N FISH según las electivas fish que tenga el estudiante
    fish_aprobadas = fish_en_pensum_ordenadas[:num_electivas_fish]
    
    # Agregar las FISH aprobadas a la lista de materias aprobadas
    aprobadas_con_fish = aprobadas + fish_aprobadas

    # Semestre máximo cursado (asegurar entero)
    try:
        semestre_max = int(pd.to_numeric(historia["semestre"], errors='coerce').max())
    except Exception:
        semestre_max = 0

    # Créditos aprobados: sumar créditos del pensum para materias aprobadas (evita doble conteo por reintentos)
    if 'créditos' in pensum.columns:
        creditos_aprobados = pensum[pensum['materia'].isin(aprobadas_con_fish)]['créditos'].sum()
    else:
        # Fallback: sumar créditos desde la historia (si existen)
        creditos_aprobados = historia.loc[historia["definitiva"] >= nota_aprobatoria, "créditos"].sum()

    # Periodos matriculados
    periodos_matriculados = historia["periodo"].nunique() if 'periodo' in historia.columns else 0

    # Verificación de "nivelado"
    nivelado = False
    niveles_config = config.get("niveles_creditos_periodos", {})
    if semestre_max in niveles_config:
        regla = niveles_config[semestre_max]
        if creditos_aprobados >= regla["min_creditos"] and periodos_matriculados <= regla["max_periodos"]:
            nivelado = True

    # Porcentaje de avance - Calcular total de créditos desde el pensum
    total_creditos = 0
    if programa_id:
        try:
            from api.pensum.repositories.repository_pensum import PensumRepository
            repo = PensumRepository()
            pensum_obj = repo.get_current_by_programa(programa_id)
            if pensum_obj:
                total_creditos = pensum_obj.creditos_obligatorios_totales
            else:
                raise ValueError(f"No se pudo obtener el pensum para programa_id={programa_id}")
        except Exception as e:
            raise ValueError(f"Error al calcular créditos del pensum: {e}")
    else:
        raise ValueError("programa_id es requerido para calcular créditos obligatorios")
    
    porcentaje_avance = creditos_aprobados / total_creditos if total_creditos else 0

    # Materias que faltan hasta el semestre límite (comparando nombres normalizados, incluyendo FISH)
    faltantes = [m for m in materias_requeridas if m not in aprobadas_con_fish]

    # Elegibilidad
    porcentaje_minimo = config.get("porcentaje_avance_minimo", 0)
    if nivelado and not faltantes:
        estado = 1
    elif porcentaje_avance >= porcentaje_minimo and semestre_max >= semestre_limite and not faltantes:
        estado = 1
    else:
        estado = 0

    return {
        "semestre_maximo": semestre_max,
        "creditos_aprobados": int(creditos_aprobados),
        "creditos_obligatorios_totales": int(total_creditos),
        "periodos_matriculados": int(periodos_matriculados),
        "porcentaje_avance": round(porcentaje_avance * 100, 2),
        "nivelado": nivelado,
        "estado": estado,
        "materias_faltantes_hasta_semestre_limite": faltantes
    }
