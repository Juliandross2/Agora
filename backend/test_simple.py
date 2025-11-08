"""
Script simple para probar el endpoint con el archivo .xls
"""
import requests

url = "http://localhost:8000/api/historias/verificar/estudiante/"

files = {
    'historia': open('test_data/historia-academica-104619021300.xls', 'rb'),
    'pensum': open('test_data/Pensum_PIS.xlsx', 'rb')
}

data = {
    'estudiante': 'historia-academica-104619021300'
}

print("📤 Enviando solicitud...")
print(f"   URL: {url}")
print(f"   Historia: test_data/historia-academica-104619021300.xls")
print(f"   Pensum: test_data/Pensum_PIS.xlsx")
print(f"   Estudiante: {data['estudiante']}\n")

try:
    response = requests.post(url, files=files, data=data)
    print(f"📥 Status Code: {response.status_code}\n")
    
    if response.status_code == 200:
        print("✅ SUCCESS\n")
        import json
        resultado = response.json()
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        
        print("\n📊 INTERPRETACIÓN:")
        print(f"   Estudiante: {resultado.get('estudiante', 'N/A')}")
        print(f"   Semestre máximo: {resultado.get('semestre_maximo', 'N/A')}")
        print(f"   Créditos aprobados: {resultado.get('creditos_aprobados', 'N/A')}")
        print(f"   Porcentaje de avance: {resultado.get('porcentaje_avance', 'N/A')}%")
        print(f"   Nivelado: {'Sí ✅' if resultado.get('nivelado') else 'No ❌'}")
        print(f"   Estado: {'ELEGIBLE ✅' if resultado.get('estado') == 1 else 'NO ELEGIBLE ❌'}")
        
        if resultado.get('materias_faltantes_hasta_semestre_limite'):
            print(f"\n   Materias faltantes ({len(resultado['materias_faltantes_hasta_semestre_limite'])}):")
            for materia in resultado['materias_faltantes_hasta_semestre_limite']:
                print(f"      - {materia}")
    else:
        print(f"❌ ERROR {response.status_code}\n")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print("❌ ERROR: No se pudo conectar al servidor")
    print("   Asegúrate de que el servidor esté corriendo:")
    print("   python manage.py runserver")
except Exception as e:
    print(f"❌ ERROR: {e}")
