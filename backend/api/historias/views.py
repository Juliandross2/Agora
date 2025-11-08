from django.http import JsonResponse
from .lector_csv import leer_pensum, leer_varias_historias
from .comparador import comparar_estudiante
import os

def verificar_elegibilidad(request):

    ruta_pensum = "historias/data/Pensum_PIS.xlsx"
    carpeta_historias = "historias/data/historias"

    if not os.path.exists(ruta_pensum):
        return JsonResponse({"error": "No se encuentra el archivo del pensum"}, status=500)

    pensum = leer_pensum(ruta_pensum)

    if not os.path.exists(carpeta_historias):
        return JsonResponse({"error": "No existe la carpeta de historias"}, status=500)

    historias = leer_varias_historias(carpeta_historias)

    resultados = []
    for historia in historias:
        archivo = historia["archivo"].iloc[0]
        nombre_estudiante = archivo.replace(".csv", "")

        result = comparar_estudiante(historia, pensum)
        result["estudiante"] = nombre_estudiante
        resultados.append(result)

    return JsonResponse(resultados, safe=False, json_dumps_params={"ensure_ascii": False, "indent": 4})
