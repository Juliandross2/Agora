"""
Script para probar el endpoint de verificación de elegibilidad de estudiantes
Asegúrate de que el servidor Django esté corriendo antes de ejecutar este script
"""
import requests
import os
import json

BASE_URL = "http://localhost:8000/api/historias"

def test_verificar_estudiante_individual():
    """
    Prueba el endpoint POST /api/historias/verificar/estudiante/
    """
    print("\n" + "="*60)
    print("TEST 1: Verificar elegibilidad de un estudiante individual")
    print("="*60)
    
    url = f"{BASE_URL}/verificar/estudiante/"
    
    # Verificar que los archivos existen
    historia_path = 'test_data/historia-academica-104619021300.xls'
    pensum_path = 'test_data/Pensum_PIS.xlsx'  # Usar el archivo real
    
    if not os.path.exists(historia_path):
        print(f"❌ ERROR: No se encuentra {historia_path}")
        print("   Ejecuta primero: python setup_test.py")
        return
    
    if not os.path.exists(pensum_path):
        print(f"❌ ERROR: No se encuentra {pensum_path}")
        print("   Copia el archivo Pensum_PIS.xlsx a test_data/")
        return
    
    try:
        # Preparar archivos para enviar
        files = {
            'historia': open(historia_path, 'rb'),
            'pensum': open(pensum_path, 'rb')
        }
        
        data = {
            'estudiante': 'historia-academica-104619021300'
        }
        
        print(f"\n📤 Enviando solicitud a: {url}")
        print(f"   - Historia: {historia_path}")
        print(f"   - Pensum: {pensum_path}")
        print(f"   - Estudiante: {data['estudiante']}")
        
        response = requests.post(url, files=files, data=data)
        
        print(f"\n📥 Respuesta recibida:")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ SUCCESS\n")
            resultado = response.json()
            print(json.dumps(resultado, indent=2, ensure_ascii=False))
            
            # Interpretación
            print("\n📊 INTERPRETACIÓN:")
            print(f"   Estudiante: {resultado.get('estudiante', 'N/A')}")
            print(f"   Semestre máximo cursado: {resultado.get('semestre_maximo')}")
            print(f"   Créditos aprobados: {resultado.get('creditos_aprobados')}")
            print(f"   Porcentaje de avance: {resultado.get('porcentaje_avance')}%")
            print(f"   ¿Está nivelado?: {'Sí ✅' if resultado.get('nivelado') else 'No ❌'}")
            
            if resultado.get('estado') == 1:
                print(f"\n   🎉 RESULTADO: ELEGIBLE PARA ELECTIVAS")
            else:
                print(f"\n   ⚠️ RESULTADO: NO ELEGIBLE PARA ELECTIVAS")
                
            if resultado.get('materias_faltantes_hasta_semestre_limite'):
                print(f"\n   Materias faltantes:")
                for materia in resultado['materias_faltantes_hasta_semestre_limite']:
                    print(f"      - {materia}")
        else:
            print(f"   ❌ ERROR\n")
            try:
                error = response.json()
                print(json.dumps(error, indent=2, ensure_ascii=False))
            except:
                print(response.text)
        
        # Cerrar archivos
        files['historia'].close()
        files['pensum'].close()
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: No se pudo conectar al servidor")
        print("   Asegúrate de que el servidor Django esté corriendo:")
        print("   python manage.py runserver")
    except Exception as e:
        print(f"\n❌ ERROR inesperado: {str(e)}")



if __name__ == "__main__":
    print("\n🧪 PRUEBAS DEL MICROSERVICIO DE HISTORIAS")
    print("="*60)
    print("Asegúrate de que el servidor esté corriendo:")
    print("  python manage.py runserver")
    print("="*60)
    
    # Ejecutar pruebas
    test_verificar_estudiante_individual()

    
    print("\n" + "="*60)
    print("✅ PRUEBAS COMPLETADAS")
    print("="*60)
