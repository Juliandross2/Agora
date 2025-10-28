import pandas as pd
import os

def leer_historias(carpeta_csv):
    historias = []
    for archivo in os.listdir(carpeta_csv):
        if archivo.endswith('.csv'):
            ruta = os.path.join(carpeta_csv, archivo)
            df = pd.read_csv(ruta, encoding='latin1', sep=',')
            df.columns = df.columns.str.strip().str.lower()
            df['archivo'] = archivo  # mantener referencia
            historias.append(df)
    return historias
