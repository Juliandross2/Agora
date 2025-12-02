import pandas as pd
import unicodedata
import re
import logging
from ..config.config import CONFIG

# Configurar logger
logger = logging.getLogger(__name__)

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
    """Normaliza textos: elimina acentos, convierte a MAYÚSCULAS y hace strip."""
    if pd.isna(s):
        return ""
    s = str(s)
    # Eliminar tildes/acentos
    s = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('utf-8')
    # Convertir a mayúsculas y quitar espacios
    return s.strip().upper()


def _es_fish(materia_nombre):
    """
    Verifica si una materia es una FISH (comienza con 'fish' seguido de espacio y número).
    
    Args:
        materia_nombre: Nombre normalizado de la materia
    
    Returns:
        True si es una FISH, False en caso contrario
    """
    patron = r'^FISH\s*\d+$'
    return bool(re.match(patron, materia_nombre.strip()))


def _es_electiva_fish(materia_nombre):
    """
    Verifica si una materia es una Electiva Fish (comienza con 'electiva fish').
    
    Args:
        materia_nombre: Nombre normalizado de la materia
    
    Returns:
        True si es una Electiva Fish, False en caso contrario
    """
    return materia_nombre.strip().startswith('ELECTIVA FISH')


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
    print("="*80)
    print("INICIO DE COMPARACIÓN DE ESTUDIANTE")
    print("="*80)
    
    # Validar que se proporcione configuración
    if config is None:
        raise ValueError("La configuración es requerida. Debe existir en la base de datos.")
    
    semestre_limite = config.get("semestre_limite_electivas")
    nota_aprobatoria = config.get("nota_aprobatoria")
    
    print(f"Configuración recibida:")
    print(f"  - Semestre límite: {semestre_limite}")
    print(f"  - Nota aprobatoria: {nota_aprobatoria}")
    print(f"  - Porcentaje mínimo: {config.get('porcentaje_avance_minimo')}")
    
    if semestre_limite is None or nota_aprobatoria is None:
        raise ValueError("La configuración está incompleta. Faltan campos requeridos.")

    # Normalizar columnas y valores de materia en pensum
    pensum.columns = pensum.columns.str.strip().str.lower()
    if 'materia' in pensum.columns:
        print(f"\n PENSUM - Materias ANTES de normalizar (primeras 5):")
        print(pensum['materia'].head().tolist())
        pensum['materia'] = pensum['materia'].apply(_normalize_text)
        print(f" PENSUM - Materias DESPUÉS de normalizar (primeras 5):")
        print(pensum['materia'].head().tolist())

    # Pensum hasta semestre límite
    pensum_limite = pensum[pensum["semestre"] <= semestre_limite]
    materias_requeridas = pensum_limite["materia"].tolist()
    print(f"\n Materias requeridas hasta semestre {semestre_limite}: {len(materias_requeridas)} materias")
    print(f"   {materias_requeridas[:10]}")  # Mostrar primeras 10

    # Normalizar valores de materia en historia
    historia.columns = historia.columns.str.strip().str.lower()
    if 'materia' in historia.columns:
        print(f"\n HISTORIA - Materias ANTES de normalizar (primeras 5):")
        print(historia['materia'].head().tolist())
        historia['materia'] = historia['materia'].apply(_normalize_text)
        print(f" HISTORIA - Materias DESPUÉS de normalizar (primeras 5):")
        print(historia['materia'].head().tolist())

    # Materias aprobadas: si en cualquier semestre la materia tiene definitiva >= nota_aprobatoria
    aprobadas = historia.loc[historia["definitiva"] >= nota_aprobatoria, "materia"].unique().tolist()
    print(f"\n Materias APROBADAS (nota >= {nota_aprobatoria}): {len(aprobadas)} materias")
    print(f"   {aprobadas[:10]}")  # Mostrar primeras 10

    # MANEJO ESPECIAL DE FISH: Contar cuántas Electivas Fish ha aprobado el estudiante
    electivas_fish_aprobadas = [m for m in aprobadas if _es_electiva_fish(m)]
    num_electivas_fish = len(electivas_fish_aprobadas)
    print(f"\n Electivas FISH aprobadas: {num_electivas_fish}")
    print(f"   {electivas_fish_aprobadas}")
    
    # Identificar las FISH en el pensum y marcarlas como aprobadas según las electivas fish del estudiante
    fish_en_pensum = []
    for materia in materias_requeridas:
        if _es_fish(materia):
            fish_en_pensum.append(materia)
    
    print(f"\n FISH en pensum: {len(fish_en_pensum)}")
    print(f"   {fish_en_pensum}")
    
    # Ordenar las FISH por número (fish 1, fish 2, fish 3, etc.)
    fish_en_pensum_ordenadas = sorted(fish_en_pensum, key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0)
    
    # Marcar como aprobadas las primeras N FISH según las electivas fish que tenga el estudiante
    fish_aprobadas = fish_en_pensum_ordenadas[:num_electivas_fish]
    print(f"\n FISH marcadas como aprobadas: {len(fish_aprobadas)}")
    print(f"   {fish_aprobadas}")
    
    # Agregar las FISH aprobadas a la lista de materias aprobadas
    aprobadas_con_fish = aprobadas + fish_aprobadas
    print(f"\n TOTAL aprobadas (con FISH): {len(aprobadas_con_fish)} materias")

    # Semestre máximo cursado (asegurar entero)
    try:
        semestre_max = int(pd.to_numeric(historia["semestre"], errors='coerce').max())
    except Exception:
        semestre_max = 0
    print(f"\n Semestre máximo cursado: {semestre_max}")

    # Créditos aprobados: sumar créditos del pensum para materias aprobadas (evita doble conteo por reintentos)
    if 'créditos' in pensum.columns:
        creditos_aprobados = pensum[pensum['materia'].isin(aprobadas_con_fish)]['créditos'].sum()
    else:
        # Fallback: sumar créditos desde la historia (si existen)
        creditos_aprobados = historia.loc[historia["definitiva"] >= nota_aprobatoria, "créditos"].sum()
    print(f" Créditos aprobados: {creditos_aprobados}")

    # Periodos matriculados
    periodos_matriculados = historia["periodo"].nunique() if 'periodo' in historia.columns else 0
    print(f" Periodos matriculados: {periodos_matriculados}")

    # Verificación de "nivelado"
    nivelado = False
    niveles_config = config.get("niveles_creditos_periodos", {})
    print(f"\n Verificación de nivelado:")
    print(f"   Niveles configurados: {niveles_config}")
    if semestre_max in niveles_config:
        regla = niveles_config[semestre_max]
        print(f"   Regla para semestre {semestre_max}: {regla}")
        print(f"   Créditos: {creditos_aprobados} >= {regla['min_creditos']}")
        print(f"   Periodos: {periodos_matriculados} <= {regla['max_periodos']}")
        if creditos_aprobados >= regla["min_creditos"] and periodos_matriculados <= regla["max_periodos"]:
            nivelado = True
            print(f"    NIVELADO")
    else:
        print(f"     No hay regla para semestre {semestre_max}")

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
    print(f"\n Porcentaje de avance: {round(porcentaje_avance * 100, 2)}%")
    print(f"   ({creditos_aprobados}/{total_creditos})")

    # Materias que faltan hasta el semestre límite (comparando nombres normalizados, incluyendo FISH)
    faltantes = [m for m in materias_requeridas if m not in aprobadas_con_fish]
    print(f"\n Materias FALTANTES hasta semestre {semestre_limite}: {len(faltantes)}")
    if faltantes:
        print(f"   {faltantes[:10]}")  # Mostrar primeras 10
        # Mostrar comparaciones detalladas para las primeras 3 faltantes
        for i, faltante in enumerate(faltantes[:3]):
            print(f"\n   Faltante #{i+1}: '{faltante}'")
            # Buscar coincidencias parciales
            similares = [a for a in aprobadas_con_fish if faltante[:5] in a or a[:5] in faltante]
            if similares:
                print(f"      Posibles similares aprobadas: {similares[:3]}")

    # Elegibilidad
    porcentaje_minimo = config.get("porcentaje_avance_minimo", 0)
    print(f"\n CRITERIOS DE ELEGIBILIDAD:")
    print(f"   Nivelado: {nivelado}")
    print(f"   Sin faltantes: {not faltantes}")
    print(f"   Porcentaje >= {porcentaje_minimo*100}%: {porcentaje_avance >= porcentaje_minimo}")
    print(f"   Semestre >= {semestre_limite}: {semestre_max >= semestre_limite}")
    
    if nivelado and not faltantes:
        estado = 1
        print(f"    ELEGIBLE (nivelado y sin faltantes)")
    elif porcentaje_avance >= porcentaje_minimo and semestre_max >= semestre_limite and not faltantes:
        estado = 1
        print(f"    ELEGIBLE (cumple todos los criterios)")
    else:
        estado = 0
        print(f"    NO ELEGIBLE")

    print("="*80)
    print("FIN DE COMPARACIÓN")
    print("="*80)

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
