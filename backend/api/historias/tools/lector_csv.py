import pandas as pd
import os

def leer_pensum(ruta_pensum: str) -> pd.DataFrame:
    """
    Lee el archivo de pensum (.xlsx) y normaliza las columnas.
    Retorna un DataFrame.
    """
    pensum = pd.read_excel(ruta_pensum)
    pensum.columns = pensum.columns.str.strip().str.lower()
    return pensum

def leer_historia(ruta_csv: str) -> pd.DataFrame:
    """
    Lee un archivo CSV de historia académica y limpia sus columnas.
    Retorna un DataFrame.
    """
    df = pd.read_csv(ruta_csv, encoding="latin1", sep=",")
    df.columns = df.columns.str.strip().str.lower()

    # Notas a número
    df["definitiva"] = pd.to_numeric(df["definitiva"], errors="coerce")

    # Normalizar nombre de materias
    df["materia"] = df["materia"].str.strip().str.lower()

    # Guardar el nombre del archivo dentro del DF (para identificar al estudiante)
    df["archivo"] = os.path.basename(ruta_csv)

    return df

def leer_varias_historias(carpeta_csv: str) -> list:
    """
    Lee todos los archivos CSV de una carpeta y retorna una lista de DataFrames,
    uno por cada estudiante.
    """
    historias = []

    for archivo in os.listdir(carpeta_csv):
        if archivo.endswith(".csv"):
            ruta = os.path.join(carpeta_csv, archivo)
            df = leer_historia(ruta)
            historias.append(df)

    return historias
