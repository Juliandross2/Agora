import pandas as pd

class LectorCSV:
    """
    Clase que encapsula la lectura y conversión del archivo CSV.
    Sirve como interfaz entre los datos y la API.
    """

    def __init__(self, ruta_archivo: str):
        self.ruta_archivo = ruta_archivo

    def leer_datos(self):
        """
        Lee el CSV y devuelve los datos como una lista de diccionarios.
        """
        try:
            df = pd.read_csv(self.ruta_archivo, encoding='latin1', sep=',')
            datos = df.to_dict(orient='records')

            # Puedes dividir la info en secciones si quieres más adelante
            # Por ejemplo: por periodo o semestre
            return datos
        except Exception as e:
            return {"error": f"No se pudo leer el archivo: {str(e)}"}
