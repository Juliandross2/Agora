from historias.lector_csv import leer_pensum, leer_varias_historias
from historias.comparador import comparar_estudiante
from historias.generador_json import guardar_json
import os

def main():
    # ========= Rutas configurables =========
    ruta_pensum = "data/Pensum_PIS.xlsx"       # Ruta al pensum
    carpeta_historias = "data/historias/"      # Carpeta con los CSV
    ruta_salida = "resultados/resultados_elegibilidad.json"  # Archivo final JSON

    print("✅ Iniciando proceso de verificación de electivas...")

    # ========= 1. Leer el pensum =========
    if not os.path.exists(ruta_pensum):
        print(f"❌ ERROR: No se encontró el archivo del pensum en {ruta_pensum}")
        return
    
    pensum = leer_pensum(ruta_pensum)
    print("📘 Pensum cargado correctamente.")

    # ========= 2. Leer todas las historias académicas =========
    if not os.path.exists(carpeta_historias):
        print(f"❌ ERROR: La carpeta {carpeta_historias} no existe.")
        return

    historias = leer_varias_historias(carpeta_historias)

    if len(historias) == 0:
        print("⚠️ No se encontraron historias académicas en la carpeta.")
        return
    
    print(f"📗 {len(historias)} historias académicas cargadas.")

    # ========= 3. Ejecutar comparador por estudiante =========
    resultados = []

    for historia in historias:
        archivo = historia["archivo"].iloc[0]
        nombre_estudiante = archivo.replace(".csv", "")

        print(f"🔎 Analizando estudiante: {nombre_estudiante}...")

        resultado = comparar_estudiante(historia, pensum)
        resultado["estudiante"] = nombre_estudiante
        resultados.append(resultado)

    # ========= 4. Guardar JSON final =========
    guardar_json(resultados, ruta_salida)

    print("\n✅ Proceso completado con éxito.")
    print(f"📁 Archivo generado: {ruta_salida}\n")


if __name__ == "__main__":
    main()
