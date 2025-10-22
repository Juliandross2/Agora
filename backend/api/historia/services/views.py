from django.http import JsonResponse
from .services.lector_csv import LectorCSV

def historia_academica(request):
    lector = LectorCSV()
    datos = lector.leer_datos()
    return JsonResponse({
        "total_registros": len(datos) if isinstance(datos, list) else 0,
        "historia_academica": datos
    }, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 2})
