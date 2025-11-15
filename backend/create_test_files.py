"""
Script para crear archivos de prueba y probar el endpoint de forma aislada
"""
import pandas as pd
import os

# Crear directorio de datos de prueba si no existe
os.makedirs('test_data', exist_ok=True)

# Crear pensum de prueba en Excel
pensum_data = {
    'Materia': [
        'Cálculo I', 'Programación I', 'Física I',  # Semestre 1
        'Álgebra Lineal', 'Cálculo II', 'Programación II',  # Semestre 2
        'Estructuras de Datos', 'Base de Datos', 'Cálculo III',  # Semestre 3
        'POO', 'Arquitectura de Software', 'Redes',  # Semestre 4
        'Sistemas Operativos', 'Ingeniería de Software', 'Compiladores',  # Semestre 5
        'IA', 'Machine Learning', 'Cloud Computing',  # Semestre 6
    ],
    'Semestre': [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
    'Créditos': [4, 3, 4, 3, 4, 3, 4, 4, 4, 3, 4, 3, 4, 4, 3, 4, 4, 3]
}

pensum_df = pd.DataFrame(pensum_data)
pensum_df.to_excel('test_data/Pensum_Test.xlsx', index=False)
print("✅ Pensum de prueba creado: test_data/Pensum_Test.xlsx")

# Verificar historia CSV
if os.path.exists('test_data/historia_estudiante_001.csv'):
    print("✅ Historia académica de prueba existe: test_data/historia_estudiante_001.csv")
    historia_df = pd.read_csv('test_data/historia_estudiante_001.csv', delimiter=';')
    print(f"\n📊 Historia tiene {len(historia_df)} materias registradas")
    print(historia_df.head())
else:
    print("❌ No se encontró historia_estudiante_001.csv")

print("\n" + "="*60)
print("Archivos de prueba listos!")
print("="*60)
print("\nAhora puedes usar estos archivos para probar el endpoint:")
print("\nOPCIÓN 1 - Usando curl (PowerShell):")
print('curl -X POST "http://localhost:8000/api/historias/verificar/estudiante/" `')
print('  -F "historia=@test_data/historia_estudiante_001.csv" `')
print('  -F "pensum=@test_data/Pensum_Test.xlsx" `')
print('  -F "estudiante=Estudiante 001"')

print("\nOPCIÓN 2 - Usando Python requests:")
print("python test_endpoint.py")

print("\nOPCIÓN 3 - Usando Swagger UI:")
print("http://localhost:8000/api/docs/swagger/")
print("Busca 'comparador-estudiantes' y prueba desde ahí")
