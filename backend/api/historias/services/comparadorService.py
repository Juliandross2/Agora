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
    materias = pensum_obj.materia_set.filter(
        es_activa=True,
        es_obligatoria=True  # solo materias obligatorias cuentan para elegibilidad
    ).values('nombre_materia', 'semestre', 'creditos')
    
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


def _roman_to_int(roman):
    """
    Convierte números romanos a enteros.
    Soporta: I, II, III, IV, V, VI, VII, VIII, IX, X
    """
    roman_values = {
        'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5,
        'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10
    }
    return roman_values.get(roman.upper(), 0)

def _int_to_roman(num):
    """
    Convierte enteros a números romanos.
    Soporta: 1-10
    """
    int_to_roman_map = {
        1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V',
        6: 'VI', 7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X'
    }
    return int_to_roman_map.get(num, str(num))

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
    Verifica si una materia es una FISH (comienza con 'FISH' seguido de número arábigo o romano).
    Ejemplos válidos: FISH 1, FISH 2, FISH I, FISH II, FISH III
    
    Args:
        materia_nombre: Nombre normalizado de la materia
    
    Returns:
        True si es una FISH, False en caso contrario
    """
    # Patrón para números arábigos: FISH 1, FISH 2, etc.
    patron_arabigo = r'^FISH\s*\d+$'
    # Patrón para números romanos: FISH I, FISH II, FISH III, etc.
    patron_romano = r'^FISH\s*[IVX]+$'
    
    materia = materia_nombre.strip()
    return bool(re.match(patron_arabigo, materia) or re.match(patron_romano, materia))


def _extraer_numero_fish(materia_nombre):
    """
    Extrae el número (como entero) de una materia FISH.
    Soporta números arábigos y romanos.
    
    Args:
        materia_nombre: Nombre normalizado de la materia FISH (ej: "FISH 1", "FISH I")
    
    Returns:
        Número entero, o 0 si no se puede extraer
    """
    materia = materia_nombre.strip()
    
    # Intentar extraer número arábigo
    match_arabigo = re.search(r'\d+', materia)
    if match_arabigo:
        return int(match_arabigo.group())
    
    # Intentar extraer número romano
    match_romano = re.search(r'[IVX]+$', materia)
    if match_romano:
        return _roman_to_int(match_romano.group())
    
    return 0


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
                Debe contener: nota_aprobatoria y semestre_limite_electivas
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

    # Pensum segmentado por semestre límite
    pensum_limite = pensum[pensum["semestre"] <= semestre_limite]
    pensum_fuera_limite = pensum[pensum["semestre"] > semestre_limite]
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
    
    print(f"\nprint FISH en pensum (hasta semestre {semestre_limite}): {len(fish_en_pensum)}")
    print(f"   {fish_en_pensum}")
    
    # Ordenar las FISH por número (soporta arábigos y romanos)
    fish_en_pensum_ordenadas = sorted(fish_en_pensum, key=_extraer_numero_fish)
    
    print(f"print FISH ordenadas: {fish_en_pensum_ordenadas}")
    
    # Marcar como aprobadas las primeras N FISH según las electivas fish que tenga el estudiante
    fish_aprobadas = fish_en_pensum_ordenadas[:num_electivas_fish]
    print(f"\nprint FISH marcadas como aprobadas (basado en {num_electivas_fish} Electivas FISH): {len(fish_aprobadas)}")
    print(f"   {fish_aprobadas}")
    
    # Agregar las FISH aprobadas a la lista de materias aprobadas
    aprobadas_con_fish = aprobadas + fish_aprobadas
    print(f"\nprint TOTAL aprobadas (con FISH): {len(aprobadas_con_fish)} materias")

    # Materias aprobadas después del semestre límite
    materias_aprobadas_fuera_limite_df = pensum_fuera_limite[
        pensum_fuera_limite['materia'].isin(aprobadas_con_fish)
    ]
    materias_aprobadas_fuera_limite = [
        {
            "materia": fila['materia'],
            "semestre": int(fila['semestre']) if pd.notna(fila['semestre']) else None,
            "creditos": int(fila['créditos']) if pd.notna(fila['créditos']) else None
        }
        for _, fila in materias_aprobadas_fuera_limite_df.iterrows()
    ]
    print(f"\n Materias aprobadas DESPUÉS del semestre límite: {len(materias_aprobadas_fuera_limite)}")

    # Semestre máximo cursado (asegurar entero)
    try:
        semestre_max = int(pd.to_numeric(historia["semestre"], errors='coerce').max())
    except Exception:
        semestre_max = 0
    print(f"\n Semestre máximo cursado: {semestre_max}")

    # Créditos aprobados: sumar solo créditos obligatorios hasta el semestre límite
    if 'créditos' in pensum_limite.columns:
        creditos_aprobados = pensum_limite[pensum_limite['materia'].isin(aprobadas_con_fish)]['créditos'].sum()
    else:
        # Fallback: sumar créditos desde la historia (si existen) respetando semestre límite
        historia_semestres = pd.to_numeric(historia["semestre"], errors='coerce')
        creditos_aprobados = historia.loc[
            (historia["definitiva"] >= nota_aprobatoria) &
            (historia_semestres <= semestre_limite),
            "créditos"
        ].sum()
    print(f" Créditos aprobados: {creditos_aprobados}")

    # Periodos matriculados
    periodos_matriculados = historia["periodo"].nunique() if 'periodo' in historia.columns else 0
    print(f" Periodos matriculados: {periodos_matriculados}")

    # Créditos requeridos hasta el semestre límite
    creditos_requeridos_hasta_limite = None
    if 'créditos' in pensum_limite.columns:
        creditos_requeridos_hasta_limite = pensum_limite['créditos'].sum()
        print(f"\n Créditos requeridos hasta semestre {semestre_limite}: {creditos_requeridos_hasta_limite}")
    else:
        print("\n No fue posible determinar los créditos requeridos (columna 'créditos' no disponible en pensum)")
    
    # Verificación de "nivelado": debe haber aprobado el 100% de los créditos obligatorios hasta el semestre límite
    nivelado = False
    if creditos_requeridos_hasta_limite is not None:
        print(f" Verificación de nivelado (créditos aprobados vs requeridos): {creditos_aprobados} >= {creditos_requeridos_hasta_limite}")
        nivelado = creditos_requeridos_hasta_limite > 0 and creditos_aprobados >= creditos_requeridos_hasta_limite
        print(f" Resultado nivelado: {nivelado}")
    else:
        print(" Resultado nivelado: No evaluado por falta de información de créditos")

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

    # Elegibilidad basada únicamente en el cumplimiento del 100% de créditos obligatorios hasta el semestre límite
    print(f"\n CRITERIOS DE ELEGIBILIDAD:")
    print(f"   Nivelado (100% créditos hasta semestre {semestre_limite}): {nivelado}")
    print(f"   Sin materias faltantes: {not faltantes}")
    
    if nivelado and not faltantes:
        estado = 1
        print("    ELEGIBLE (cumple créditos y no tiene faltantes)")
    else:
        estado = 0
        print("    NO ELEGIBLE")

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
        "materias_faltantes_hasta_semestre_limite": faltantes,
        "materias_aprobadas_despues_semestre_limite": materias_aprobadas_fuera_limite
    }
