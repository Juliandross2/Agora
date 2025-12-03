import requests
import os

def test_verificar_historia():
    url = "http://localhost:8000/api/historias/verificar/estudiante/"
    
    # Rutas a los archivos
    base_dir = os.path.dirname(os.path.abspath(__file__))
    historia_path = os.path.join(base_dir, "test_data", "historia_estudiante_001.csv")
    pensum_path = os.path.join(base_dir, "test_data", "Pensum_PIS.xlsx")
    
    # Verificar que los archivos existen
    if not os.path.exists(historia_path) or not os.path.exists(pensum_path):
        print(f"Error: No se encuentran los archivos de prueba")
        return
    
    # Preparar los archivos
    files = {
        'historia': ('historia.csv', open(historia_path, 'rb'), 'text/csv'),
        'pensum': ('pensum.xlsx', open(pensum_path, 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    }
    
    # Datos adicionales
    data = {
        'estudiante': 'Estudiante de prueba'
    }
    
    try:
        # Hacer la petición POST
        print("Enviando archivos...")
        response = requests.post(url, files=files, data=data)
        
        # Imprimir resultado
        print(f"\nCódigo de respuesta: {response.status_code}")
        print("\nRespuesta del servidor:")
        print(response.json())
        
    except Exception as e:
        print(f"Error al hacer la petición: {str(e)}")
    finally:
        # Cerrar los archivos
        for f in files.values():
            f[1].close()

if __name__ == "__main__":
    test_verificar_historia()