from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, inline_serializer
from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
import json
import pandas as pd
import os

from api.historias.services.comparadorService import comparar_estudiante
from api.historias.tools.lector_csv import leer_pensum, leer_varias_historias


@extend_schema(
	request=inline_serializer(
		name='VerificarElegibilidadRequest',
		fields={
			'historia': serializers.FileField(help_text='Archivo CSV o Excel (.csv, .xls, .xlsx) con la historia académica. Columnas: Materia;Semestre;Créditos;Definitiva;Periodo;archivo'),
			'pensum': serializers.FileField(help_text='Archivo Excel (.xlsx) con el pensum. Columnas: Materia, Semestre, Créditos'),
			'estudiante': serializers.CharField(required=False, help_text='Nombre del estudiante (opcional)'),
		}
	),
	responses={
		200: OpenApiResponse(
			description="Elegibilidad verificada exitosamente",
			examples=[
				OpenApiExample(
					'Ejemplo de respuesta exitosa',
					value={
						"semestre_maximo": 5,
						"creditos_aprobados": 56,
						"periodos_matriculados": 5,
						"porcentaje_avance": 35.22,
						"nivelado": False,
						"estado": 0,
						"materias_faltantes_hasta_semestre_limite": ["ia", "machine learning"],
						"estudiante": "Juan Perez"
					}
				)
			]
		),
		400: OpenApiResponse(
			description="Datos inválidos o incompletos",
			examples=[
				OpenApiExample(
					'Archivos faltantes',
					value={
						"error": "Se requieren los archivos \"historia\" (CSV) y \"pensum\" (Excel)"
					}
				)
			]
		),
		500: OpenApiResponse(description="Error interno del servidor")
	},
	tags=['comparador-estudiantes'],
	summary="Verificar elegibilidad de estudiante",
	description="""
	Verifica la elegibilidad de un estudiante para cursar electivas.
	
	**Formato de archivos:**
	
	**Historia (CSV con delimitador ;):**
	```
	Materia;Semestre;Créditos;Definitiva;Periodo;archivo
	Cálculo I;1;4;4.5;2023-1;estudiante.csv
	```
	
	**Pensum (Excel):**
	| Materia | Semestre | Créditos |
	|---------|----------|----------|
	| Cálculo I | 1 | 4 |
	
	**Criterios de elegibilidad:**
	- Porcentaje mínimo de avance
	- Semestre límite alcanzado
	- Sin materias pendientes hasta el semestre límite
	- Opcionalmente estar "nivelado"
	
	**Respuesta:**
	- estado: 1 = Elegible, 0 = No elegible
	"""
)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def verificar_elegibilidad_estudiante(request):
	"""
	Verifica la elegibilidad de un estudiante para cursar electivas.
	Requiere enviar la historia académica (CSV) y el pensum en el body.
	"""
	try:
		# Debug: Ver qué datos llegan
		print(f"[DEBUG] request.FILES: {request.FILES}")
		print(f"[DEBUG] request.POST: {request.POST}")
		print(f"[DEBUG] request.data: {request.data}")
		print(f"[DEBUG] Content-Type: {request.content_type}")
		
		# Swagger UI no puede enviar archivos binarios correctamente, solo text/strings
		# Por eso, si vienen en POST, asumimos que son rutas de archivos del servidor
		if 'historia' in request.FILES and 'pensum' in request.FILES:
			# Caso normal: archivos binarios desde Postman, curl, etc.
			historia_file = request.FILES['historia']
			pensum_file = request.FILES['pensum']
			print(f"[DEBUG] Archivos recibidos en FILES")
			
		elif 'historia' in request.POST and 'pensum' in request.POST:
			# Caso Swagger: cuando solo vienen rutas en POST
			historia_path = request.POST.get('historia')
			pensum_path = request.POST.get('pensum')
			print(f"[DEBUG] Rutas recibidas - Historia: {historia_path}, Pensum: {pensum_path}")
			
			# Verificar si son rutas del servidor que existen
			if os.path.exists(historia_path) and os.path.exists(pensum_path):
				historia_file = open(historia_path, 'rb')
				pensum_file = open(pensum_path, 'rb')
				print(f"[DEBUG] Archivos abiertos desde rutas del servidor")
			else:
				return Response({
					'error': 'Swagger UI tiene limitaciones para subir archivos binarios',
					'solucion': 'Usa una de estas opciones:',
					'opciones': [
						'1. Postman: Más fácil para subir archivos',
						'2. curl: curl -F "historia=@ruta/archivo.csv" -F "pensum=@ruta/archivo.xlsx" http://localhost:8000/api/historias/verificar/estudiante/',
						'3. Script Python: python test_endpoint.py'
					],
					'nota': 'Coloca tus archivos en test_data/ y usa el script test_endpoint.py'
				}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({
				'error': 'Se requieren los archivos "historia" (CSV) y "pensum" (Excel)',
				'recibidos': {
					'FILES': list(request.FILES.keys()),
					'POST': list(request.POST.keys())
				},
				'instrucciones': 'Usa Postman, curl o el script test_endpoint.py para enviar archivos'
			}, status=status.HTTP_400_BAD_REQUEST)

		historia_file = request.FILES['historia']
		pensum_file = request.FILES['pensum']
		
		print(f"[DEBUG] Historia file: {historia_file.name}")
		print(f"[DEBUG] Pensum file: {pensum_file.name}")

		# Leer los archivos
		try:
			# Intentar leer como CSV primero
			if historia_file.name.endswith('.csv'):
				historia = pd.read_csv(historia_file, delimiter=';', encoding='latin-1')
			elif historia_file.name.endswith(('.xls', '.xlsx')):
				# Si es Excel, leerlo como Excel
				historia = pd.read_excel(historia_file)
			else:
				# Por defecto intentar CSV
				historia = pd.read_csv(historia_file, delimiter=';', encoding='latin-1')
			print(f"[DEBUG] Historia cargada: {len(historia)} filas")
		except Exception as e:
			return Response({
				'error': 'Error al leer archivo de historia',
				'details': str(e)
			}, status=status.HTTP_400_BAD_REQUEST)
		
		try:
			pensum = pd.read_excel(pensum_file)
			print(f"[DEBUG] Pensum cargado: {len(pensum)} filas")
		except Exception as e:
			return Response({
				'error': 'Error al leer archivo de pensum',
				'details': str(e)
			}, status=status.HTTP_400_BAD_REQUEST)

		# Normalizar columnas
		historia.columns = historia.columns.str.strip().str.lower()
		pensum.columns = pensum.columns.str.strip().str.lower()
		
		print(f"[DEBUG] Columnas historia: {list(historia.columns)}")
		print(f"[DEBUG] Columnas pensum: {list(pensum.columns)}")

		# Ejecutar comparación
		resultado = comparar_estudiante(historia, pensum)
		
		# Agregar información adicional si se proporciona
		if 'estudiante' in request.POST:
			resultado['estudiante'] = request.POST.get('estudiante')

		print(f"[DEBUG] Resultado: {resultado}")
		return Response(resultado, status=status.HTTP_200_OK)

	except KeyError as e:
		return Response({
			'error': 'Columna faltante en los archivos',
			'details': f'No se encontró la columna: {str(e)}'
		}, status=status.HTTP_400_BAD_REQUEST)
	except Exception as e:
		print(f"[ERROR] Exception: {type(e).__name__}: {str(e)}")
		import traceback
		traceback.print_exc()
		return Response({
			'error': 'Error al procesar la solicitud',
			'details': str(e)
		}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
	request=None,
	responses={
		200: OpenApiResponse(description="Elegibilidad verificada para múltiples estudiantes"),
		500: OpenApiResponse(description="Error interno del servidor")
	},
	tags=['comparador-estudiantes'],
	description="Verifica la elegibilidad de múltiples estudiantes usando archivos almacenados en el servidor"
)
@api_view(['GET'])
def verificar_elegibilidad_masiva(request):
	"""
	Verifica la elegibilidad de todos los estudiantes cuyas historias estén 
	almacenadas en la carpeta de historias del servidor.
	"""
	try:
		ruta_pensum = "historias/data/Pensum_PIS.xlsx"
		carpeta_historias = "historias/data/historias"

		# Validar que existan los archivos
		if not os.path.exists(ruta_pensum):
			return Response({
				'error': 'No se encuentra el archivo del pensum en el servidor'
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		if not os.path.exists(carpeta_historias):
			return Response({
				'error': 'No existe la carpeta de historias en el servidor'
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		# Leer pensum
		pensum = leer_pensum(ruta_pensum)

		# Leer todas las historias
		historias = leer_varias_historias(carpeta_historias)

		if len(historias) == 0:
			return Response({
				'mensaje': 'No se encontraron historias académicas',
				'resultados': []
			}, status=status.HTTP_200_OK)

		# Procesar cada estudiante
		resultados = []
		for historia in historias:
			archivo = historia["archivo"].iloc[0]
			nombre_estudiante = archivo.replace(".csv", "")

			resultado = comparar_estudiante(historia, pensum)
			resultado["estudiante"] = nombre_estudiante
			resultados.append(resultado)

		return Response({
			'total_estudiantes': len(resultados),
			'resultados': resultados
		}, status=status.HTTP_200_OK)

	except Exception as e:
		return Response({
			'error': 'Error al verificar elegibilidad masiva',
			'details': str(e)
		}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
	request=None,
	responses={
		200: OpenApiResponse(description="Estadísticas generadas exitosamente"),
		500: OpenApiResponse(description="Error interno del servidor")
	},
	tags=['comparador-estudiantes'],
	description="Obtiene estadísticas generales de elegibilidad de los estudiantes"
)
@api_view(['GET'])
def obtener_estadisticas_elegibilidad(request):
	"""
	Retorna estadísticas generales sobre la elegibilidad de estudiantes,
	como cantidad de elegibles, no elegibles, promedios, etc.
	"""
	try:
		ruta_pensum = "historias/data/Pensum_PIS.xlsx"
		carpeta_historias = "historias/data/historias"

		if not os.path.exists(ruta_pensum) or not os.path.exists(carpeta_historias):
			return Response({
				'error': 'Archivos del sistema no encontrados'
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		pensum = leer_pensum(ruta_pensum)
		historias = leer_varias_historias(carpeta_historias)

		if len(historias) == 0:
			return Response({
				'total_estudiantes': 0,
				'elegibles': 0,
				'no_elegibles': 0
			}, status=status.HTTP_200_OK)

		# Calcular estadísticas
		total = len(historias)
		elegibles = 0
		no_elegibles = 0
		nivelados = 0
		suma_creditos = 0
		suma_porcentaje = 0

		for historia in historias:
			resultado = comparar_estudiante(historia, pensum)
			
			if resultado['estado'] == 1:
				elegibles += 1
			else:
				no_elegibles += 1
			
			if resultado['nivelado']:
				nivelados += 1
			
			suma_creditos += resultado['creditos_aprobados']
			suma_porcentaje += resultado['porcentaje_avance']

		estadisticas = {
			'total_estudiantes': total,
			'elegibles': elegibles,
			'no_elegibles': no_elegibles,
			'porcentaje_elegibles': round((elegibles / total) * 100, 2) if total > 0 else 0,
			'estudiantes_nivelados': nivelados,
			'promedio_creditos_aprobados': round(suma_creditos / total, 2) if total > 0 else 0,
			'promedio_porcentaje_avance': round(suma_porcentaje / total, 2) if total > 0 else 0
		}

		return Response(estadisticas, status=status.HTTP_200_OK)

	except Exception as e:
		return Response({
			'error': 'Error al generar estadísticas',
			'details': str(e)
		}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
