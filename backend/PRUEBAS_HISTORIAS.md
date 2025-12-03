# Cómo Probar el Microservicio de Historias en Solitario

## ✅ Archivos de Prueba Creados

- `test_data/historia_estudiante_001.csv` - Historia académica de ejemplo
- `test_data/Pensum_Test.xlsx` - Pensum de programa de ejemplo

## 📝 Pasos para Probar

### Paso 1: Inicia el servidor Django

```powershell
python manage.py runserver
```

El servidor debería iniciar en: `http://localhost:8000`

### Paso 2: Ejecuta las Pruebas Automáticas

```powershell
python test_endpoint.py
```

Este script probará automáticamente los 3 endpoints:
1. Verificar estudiante individual (POST con archivos)
2. Verificar masivamente (GET)
3. Obtener estadísticas (GET)

## 🧪 Pruebas Manuales

### Opción A: Usar Swagger UI (MÁS FÁCIL)

1. Abre tu navegador en: `http://localhost:8000/api/docs/swagger/`
2. Busca la sección **"comparador-estudiantes"**
3. Haz clic en el endpoint **POST /api/historias/verificar/estudiante/**
4. Haz clic en "Try it out"
5. Sube los archivos:
   - **historia**: Selecciona `test_data/historia_estudiante_001.csv`
   - **pensum**: Selecciona `test_data/Pensum_Test.xlsx`
   - **estudiante**: Escribe "Juan Perez" (opcional)
6. Haz clic en "Execute"
7. Ver la respuesta abajo

### Opción B: Usar PowerShell con curl

```powershell
curl -X POST "http://localhost:8000/api/historias/verificar/estudiante/" `
  -F "historia=@test_data/historia_estudiante_001.csv" `
  -F "pensum=@test_data/Pensum_Test.xlsx" `
  -F "estudiante=Juan Perez"
```

### Opción C: Usar Postman

1. Método: **POST**
2. URL: `http://localhost:8000/api/historias/verificar/estudiante/`
3. En **Body** → selecciona **form-data**
4. Agrega:
   - Key: `historia` → Type: **File** → Selecciona `test_data/historia_estudiante_001.csv`
   - Key: `pensum` → Type: **File** → Selecciona `test_data/Pensum_Test.xlsx`
   - Key: `estudiante` → Type: **Text** → Valor: "Juan Perez"
5. Click **Send**

## 📊 Respuesta Esperada

```json
{
  "semestre_maximo": 5,
  "creditos_aprobados": 56,
  "periodos_matriculados": 5,
  "porcentaje_avance": 35.22,
  "nivelado": false,
  "estado": 0,
  "materias_faltantes_hasta_semestre_limite": [
    "ia",
    "machine learning",
    "cloud computing"
  ],
  "estudiante": "Juan Perez"
}
```

### Interpretación de la Respuesta:

- **semestre_maximo**: Último semestre cursado
- **creditos_aprobados**: Total de créditos aprobados
- **periodos_matriculados**: Número de periodos matriculados
- **porcentaje_avance**: Porcentaje de avance en el programa
- **nivelado**: Si cumple con los requisitos de nivelación
- **estado**: 1 = Elegible, 0 = No elegible
- **materias_faltantes_hasta_semestre_limite**: Materias que faltan hasta el semestre límite

## 🔧 Troubleshooting

### Error: "Can't connect to server"
**Solución**: Asegúrate de que MySQL esté corriendo y el servidor Django esté iniciado.

### Error: "No module named 'pandas'"
**Solución**: 
```powershell
pip install pandas openpyxl
```

### Error: "No se encuentra el archivo"
**Solución**: Ejecuta primero:
```powershell
python setup_test.py
```

### Error 404 al acceder al endpoint
**Solución**: Verifica que la URL incluya `/api/historias/` correctamente.

## 📁 Estructura de Archivos de Prueba

### Historia Académica (CSV):
```csv
Materia;Semestre;Créditos;Definitiva;Periodo;archivo
Cálculo I;1;4;4.5;2023-1;estudiante_001.csv
Programación I;1;3;4.2;2023-1;estudiante_001.csv
```

### Pensum (Excel):
| Materia | Semestre | Créditos |
|---------|----------|----------|
| Cálculo I | 1 | 4 |
| Programación I | 1 | 3 |

## 🎯 Endpoints Disponibles

1. **POST** `/api/historias/verificar/estudiante/`
   - Verifica un estudiante enviando archivos
   
2. **GET** `/api/historias/verificar/masiva/`
   - Verifica todos los estudiantes del servidor
   
3. **GET** `/api/historias/estadisticas/`
   - Obtiene estadísticas generales

## 📝 Notas

- Los archivos de prueba ya están creados en `test_data/`
- El CSV usa punto y coma (;) como separador
- El servidor debe estar corriendo en el puerto 8000
- Swagger UI es la forma más fácil de probar
