import pandas as pd
import os

print("="*60)
print("VERIFICACION DE ARCHIVOS DE PRUEBA REALES")
print("="*60)

# Verificar que existe la carpeta test_data
if not os.path.exists('test_data'):
    print("\nCreando carpeta test_data...")
    os.makedirs('test_data')
else:
    print("\nCarpeta test_data encontrada")

# Archivos reales de prueba
historia_path = 'test_data/historia_estudiante_001.csv'
pensum_path = 'test_data/Pensum_PIS.xlsx'

print("\n" + "-"*60)
print("Verificando archivos reales:")
print("-"*60)

# Verificar historia CSV
if os.path.exists(historia_path):
    print(f"\n✓ Historia encontrada: {historia_path}")
    try:
        historia_df = pd.read_csv(historia_path, delimiter=';', encoding='latin-1')
        print(f"  - Materias registradas: {len(historia_df)}")
        print(f"  - Columnas: {list(historia_df.columns)}")
        print(f"\n  Primeras 3 filas:")
        print(historia_df.head(3).to_string(index=False))
        
        # Estadísticas básicas
        if 'Definitiva' in historia_df.columns:
            aprobadas = len(historia_df[historia_df['Definitiva'] >= 3.0])
            print(f"\n  - Materias aprobadas (>=3.0): {aprobadas}")
        if 'Semestre' in historia_df.columns:
            print(f"  - Semestre máximo: {historia_df['Semestre'].max()}")
        if 'Créditos' in historia_df.columns:
            print(f"  - Total créditos cursados: {historia_df['Créditos'].sum()}")
            
    except Exception as e:
        print(f"  ✗ Error al leer historia: {e}")
else:
    print(f"\n✗ Historia NO encontrada: {historia_path}")
    print("  Por favor, copia tu archivo historia_estudiante_001.csv a test_data/")

# Verificar pensum Excel
if os.path.exists(pensum_path):
    print(f"\n✓ Pensum encontrado: {pensum_path}")
    try:
        pensum_df = pd.read_excel(pensum_path)
        print(f"  - Materias en pensum: {len(pensum_df)}")
        print(f"  - Columnas: {list(pensum_df.columns)}")
        
        if 'Semestre' in pensum_df.columns:
            semestres = pensum_df['Semestre'].unique()
            print(f"  - Semestres: {sorted(semestres)}")
        if 'Créditos' in pensum_df.columns or 'Creditos' in pensum_df.columns:
            col_creditos = 'Créditos' if 'Créditos' in pensum_df.columns else 'Creditos'
            print(f"  - Total créditos programa: {pensum_df[col_creditos].sum()}")
            
        print(f"\n  Primeras 3 materias:")
        print(pensum_df.head(3).to_string(index=False))
        
    except Exception as e:
        print(f"  ✗ Error al leer pensum: {e}")
else:
    print(f"\n✗ Pensum NO encontrado: {pensum_path}")
    print("  Por favor, copia tu archivo Pensum_PIS.xlsx a test_data/")

# Resumen final
print("\n" + "="*60)
print("RESUMEN")
print("="*60)

archivos_ok = os.path.exists(historia_path) and os.path.exists(pensum_path)

if archivos_ok:
    print("\n✓ Todos los archivos necesarios están presentes")
    print("\nPara probar el endpoint, ejecuta:")
    print("  1. Inicia el servidor: python manage.py runserver")
    print("  2. Ejecuta el test: python test_endpoint.py")
else:
    print("\n✗ Faltan archivos")
    print("\nColoca los archivos en test_data/:")
    if not os.path.exists(historia_path):
        print("  - historia_estudiante_001.csv")
    if not os.path.exists(pensum_path):
        print("  - Pensum_PIS.xlsx")

print("\n" + "="*60)

