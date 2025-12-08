from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, inline_serializer
from rest_framework import serializers
import pandas as pd
import os
import re
import logging

from api.historias.services.comparadorService import comparar_estudiante, obtener_pensum_desde_bd
from api.configuracion.models.configuracion_elegibilidad import ConfiguracionElegibilidad
from api.configuracion.controllers.configuracionController import obtener_configuracion

# Configurar logger
logger = logging.getLogger(__name__)

# Constantes
MAX_FILES_MASIVA = 50  # Límite de archivos en carga masiva


@extend_schema(
	request=inline_serializer(
		name='VerificarElegibilidadRequest',
		fields={
			'historia': serializers.FileField(help_text='Archivo CSV o Excel (.csv, .xls, .xlsx) con la historia académica. El código del estudiante se extrae automáticamente del nombre del archivo (formato: Historia-Academica-CODIGO.csv)'),
			'programa_id': serializers.IntegerField(required=True, help_text='ID del programa académico (requerido). Se obtiene el pensum activo y la configuración de elegibilidad desde la BD'),
		}
	),
	responses={
		200: OpenApiResponse(
			description="Elegibilidad verificada exitosamente",
			examples=[
				OpenApiExample(
					'Ejemplo de respuesta exitosa',
					value={
						"estudiante": "12345678",
						"semestre_maximo": 5,
						"creditos_aprobados": 56,
						"creditos_obligatorios_totales": 151,
						"periodos_matriculados": 5,
						"porcentaje_avance": 35.22,
						"nivelado": False,
						"estado": 0,
						"materias_faltantes_hasta_semestre_limite": ["IA", "MACHINE LEARNING"],
						"materias_aprobadas_despues_semestre_limite": [
							{"materia": "PROYECTO DE GRADO", "semestre": 10, "creditos": 3}
						]
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
	
	**Nombre del archivo:**
	El código del estudiante se extrae automáticamente del nombre del archivo.
	Formato esperado: `Historia-Academica-CODIGO.csv` (ej: Historia-Academica-12345678.csv)
	
	**Pensum y Configuración:**
	El pensum y la configuración de elegibilidad se obtienen automáticamente desde la base de datos 
	usando el `programa_id` proporcionado. 
	
	**IMPORTANTE:** Debe existir una configuración en BD para el programa. Si no existe, el endpoint 
	retornará un error 400. Crear configuración: POST /api/configuracion/crear/
	
	**Criterios de elegibilidad:**
	- Porcentaje mínimo de avance
	- Semestre límite alcanzado
	- Sin materias pendientes hasta el semestre límite
	- Opcionalmente estar "nivelado"
	
	**Respuesta:**
	- estudiante: Código del estudiante extraído del nombre del archivo (primer campo)
	- semestre_maximo: Semestre máximo cursado
	- creditos_aprobados: Total de créditos aprobados por el estudiante
	- creditos_obligatorios_totales: Total de créditos obligatorios del pensum
	- periodos_matriculados: Número de períodos matriculados
	- porcentaje_avance: Porcentaje de avance en el programa (creditos_aprobados / creditos_obligatorios_totales * 100)
	- nivelado: Si el estudiante está nivelado según la configuración
	- estado: 1 = Elegible, 0 = No elegible
	- materias_faltantes_hasta_semestre_limite: Lista de materias pendientes
	- materias_aprobadas_despues_semestre_limite: Materias obligatorias aprobadas en semestres superiores al límite
	"""
)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def verificar_elegibilidad_estudiante(request):
	"""
	Verifica la elegibilidad de un estudiante para cursar electivas.
	Requiere enviar la historia académica (CSV) y el programa_id.
	El pensum se obtiene automáticamente desde la base de datos.
	El código del estudiante se extrae automáticamente del nombre del archivo.
	"""
	try:
		# Validar que se proporcione el programa_id (requerido)
		programa_id = None
		if 'programa_id' in request.POST:
			try:
				programa_id = int(request.POST.get('programa_id'))
			except (ValueError, TypeError):
				return Response({
					'error': 'programa_id inválido o faltante',
					'details': 'El campo programa_id es requerido y debe ser un número entero'
				}, status=status.HTTP_400_BAD_REQUEST)
		elif hasattr(request, 'data') and 'programa_id' in request.data:
			try:
				programa_id = int(request.data.get('programa_id'))
			except (ValueError, TypeError):
				return Response({
					'error': 'programa_id inválido o faltante',
					'details': 'El campo programa_id es requerido y debe ser un número entero'
				}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({
				'error': 'programa_id es requerido',
				'details': 'Debe proporcionar el ID del programa académico para obtener el pensum desde la base de datos'
			}, status=status.HTTP_400_BAD_REQUEST)
		
		# Obtener pensum desde la base de datos
		try:
			pensum = obtener_pensum_desde_bd(programa_id)
		except ValueError as e:
			return Response({
				'error': 'Error al obtener pensum desde la base de datos',
				'details': str(e)
			}, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response({
				'error': 'Error inesperado al obtener pensum',
				'details': str(e)
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		
		# Validar que se proporcione el archivo de historia
		if 'historia' not in request.FILES and 'historia' not in request.POST:
			return Response({
				'error': 'Se requiere el archivo "historia" (CSV o Excel)',
				'recibidos': {
					'FILES': list(request.FILES.keys()),
					'POST': list(request.POST.keys())
				},
				'instrucciones': 'Usa Postman, curl o el script test_endpoint.py para enviar el archivo de historia'
			}, status=status.HTTP_400_BAD_REQUEST)
		
		# Leer archivo de historia
		historia_file = None
		historia_filename = None
		archivo_abierto_manual = False
		if 'historia' in request.FILES:
			historia_file = request.FILES['historia']
			historia_filename = historia_file.name
		elif 'historia' in request.POST:
			historia_path = request.POST.get('historia')
			if os.path.exists(historia_path):
				historia_file = open(historia_path, 'rb')
				historia_filename = os.path.basename(historia_path)
				archivo_abierto_manual = True
			else:
				return Response({
					'error': 'Swagger UI tiene limitaciones para subir archivos binarios',
					'solucion': 'Usa una de estas opciones:',
					'opciones': [
						'1. Postman: Más fácil para subir archivos',
						'2. curl: curl -F "historia=@ruta/archivo.csv" -F "programa_id=1" http://localhost:8000/api/historias/verificar/estudiante/',
						'3. Script Python: python test_endpoint.py'
					]
				}, status=status.HTTP_400_BAD_REQUEST)
		
		# Leer el archivo de historia
		try:
			if historia_filename and historia_filename.endswith('.csv'):
				historia = pd.read_csv(historia_file, delimiter=';', encoding='latin-1')
			elif historia_filename and historia_filename.endswith('.xlsx'):
				historia = pd.read_excel(historia_file, engine='openpyxl')
			elif historia_filename and historia_filename.endswith('.xls'):
				historia = pd.read_excel(historia_file, engine='xlrd')
			else:
				# Por defecto intentar CSV
				historia = pd.read_csv(historia_file, delimiter=';', encoding='latin-1')
		except Exception as e:
			return Response({
				'error': 'Error al leer archivo de historia',
				'details': str(e)
			}, status=status.HTTP_400_BAD_REQUEST)
		finally:
			# Cerrar el archivo si fue abierto manualmente
			if archivo_abierto_manual and historia_file:
				try:
					historia_file.close()
				except:
					pass

		# Normalizar columnas
		historia.columns = historia.columns.str.strip().str.lower()

		# Extraer código del estudiante desde el nombre del archivo
		codigo_estudiante = None
		if historia_filename:
			# Patrón para Historia-Academica-CODIGO.csv o Historia-Academica_CODIGO.csv
			match = re.search(r'Historia-Academica[_-]?(\d+)', historia_filename, re.IGNORECASE)
			if match:
				codigo_estudiante = match.group(1)
			else:
				# Si no coincide con el patrón, usar el nombre del archivo sin extensión
				codigo_estudiante = os.path.splitext(historia_filename)[0]

		# Obtener configuración desde BD
		try:
			config = obtener_configuracion(programa_id=programa_id)
		except ValueError as e:
			return Response({
				'error': 'Configuración no encontrada',
				'details': str(e)
			}, status=status.HTTP_400_BAD_REQUEST)
		
		# Ejecutar comparación con la configuración obtenida
		resultado = comparar_estudiante(historia, pensum, config=config, programa_id=programa_id)
		
		resultado_ordenado = {}
		if codigo_estudiante:
			resultado_ordenado['estudiante'] = codigo_estudiante
		resultado_ordenado.update(resultado)

		return Response(resultado_ordenado, status=status.HTTP_200_OK)

	except KeyError as e:
		return Response({
			'error': 'Columna faltante en los archivos',
			'details': f'No se encontró la columna: {str(e)}'
		}, status=status.HTTP_400_BAD_REQUEST)
	except Exception as e:
		logger.error(f"Exception en verificación individual: {type(e).__name__}: {str(e)}", exc_info=True)
		return Response({
			'error': 'Error al procesar la solicitud',
			'details': str(e)
		}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
	request=inline_serializer(
		name='VerificarElegibilidadMasivaWebRequest',
		fields={
			'historias': serializers.ListField(
				child=serializers.FileField(),
				help_text='Múltiples archivos CSV o Excel con historias académicas. Cada archivo debe tener formato: Historia-Academica-CODIGO.csv'
			),
			'programa_id': serializers.IntegerField(required=True, help_text='ID del programa académico (requerido). Se obtiene el pensum activo y la configuración de elegibilidad desde la BD'),
		}
	),
	responses={
		200: OpenApiResponse(
			description="Elegibilidad verificada para múltiples estudiantes",
			examples=[
				OpenApiExample(
					'Ejemplo de respuesta exitosa',
					value={
						"total_estudiantes": 2,
						"elegibles": 1,
						"no_elegibles": 1,
						"resultados": [
							{
								"estudiante": "12345678",
								"semestre_maximo": 9,
								"creditos_aprobados": 123,
								"creditos_obligatorios_totales": 151,
								"periodos_matriculados": 13,
								"porcentaje_avance": 81.46,
								"nivelado": False,
								"estado": 1,
								"materias_faltantes_hasta_semestre_limite": [],
								"materias_aprobadas_despues_semestre_limite": [
									{"materia": "ELECTIVA PROFESIONAL I", "semestre": 10, "creditos": 3}
								]
							},
							{
								"estudiante": "87654321",
								"semestre_maximo": 7,
								"creditos_aprobados": 90,
								"creditos_obligatorios_totales": 151,
								"periodos_matriculados": 10,
								"porcentaje_avance": 59.6,
								"nivelado": False,
								"estado": 0,
								"materias_faltantes_hasta_semestre_limite": ["CALCULO III"],
								"materias_aprobadas_despues_semestre_limite": []
							}
						]
					}
				)
			]
		),
		400: OpenApiResponse(description="Datos inválidos o incompletos"),
		500: OpenApiResponse(description="Error interno del servidor")
	},
	tags=['comparador-estudiantes'],
	summary="Verificar elegibilidad masiva (Web)",
	description="""
	Verifica la elegibilidad de múltiples estudiantes en una sola petición.
	
	**Uso típico desde la web:**
	1. El usuario selecciona múltiples archivos CSV de historias académicas
	2. Los envía en un formulario multipart/form-data
	3. El servidor procesa todos y retorna los resultados
	
	**Formato de los archivos:**
	- Cada archivo debe ser CSV con delimitador `;` o Excel (.xlsx, .xls)
	- Nombre sugerido: Historia-Academica-CODIGO.csv
	- El código del estudiante se extrae del nombre del archivo
	- Límite máximo: 50 archivos por petición
	
	**Configuración:**
	La configuración de elegibilidad se obtiene desde la BD. Debe existir una configuración 
	activa para el programa. Para crearla/modificarla: POST /api/configuracion/crear/
	
	**Respuesta:**
	- total_estudiantes: Cantidad total procesada
	- elegibles: Cantidad de estudiantes elegibles
	- no_elegibles: Cantidad de estudiantes no elegibles
	- resultados: Array con el detalle de cada estudiante
	"""
)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def verificar_elegibilidad_masiva(request):
	"""
	Verifica la elegibilidad de múltiples estudiantes subidos desde la web.
	Procesa todos los archivos en memoria y retorna los resultados.
	"""
	try:
		# Validar programa_id
		programa_id = None
		if 'programa_id' in request.POST:
			try:
				programa_id = int(request.POST.get('programa_id'))
			except (ValueError, TypeError):
				return Response({
					'error': 'programa_id inválido o faltante',
					'details': 'El campo programa_id es requerido y debe ser un número entero'
				}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({
				'error': 'programa_id es requerido',
				'details': 'Debe proporcionar el ID del programa académico'
			}, status=status.HTTP_400_BAD_REQUEST)
		
		# Obtener pensum desde la base de datos
		try:
			pensum = obtener_pensum_desde_bd(programa_id)
		except ValueError as e:
			return Response({
				'error': 'Error al obtener pensum desde la base de datos',
				'details': str(e)
			}, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response({
				'error': 'Error inesperado al obtener pensum',
				'details': str(e)
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		
		# Obtener todos los archivos de historias
		historias_files = request.FILES.getlist('historias')
		
		if not historias_files:
			return Response({
				'error': 'No se recibieron archivos de historias',
				'details': 'Debe enviar al menos un archivo en el campo "historias"',
				'ejemplo': 'Usar <input type="file" name="historias" multiple> en el formulario'
			}, status=status.HTTP_400_BAD_REQUEST)
		
		# Validar límite de archivos
		if len(historias_files) > MAX_FILES_MASIVA:
			return Response({
				'error': 'Demasiados archivos',
				'details': f'Máximo permitido: {MAX_FILES_MASIVA} archivos. Recibidos: {len(historias_files)}',
				'sugerencia': 'Divida la carga en múltiples peticiones'
			}, status=status.HTTP_400_BAD_REQUEST)
		
		# Obtener configuración desde BD
		try:
			config = obtener_configuracion(programa_id=programa_id)
		except ValueError as e:
			return Response({
				'error': 'Configuración no encontrada',
				'details': str(e)
			}, status=status.HTTP_400_BAD_REQUEST)
		
		# Procesar cada archivo
		resultados = []
		archivos_con_error = []
		
		for archivo in historias_files:
			try:
				nombre_archivo = archivo.name
				
				# Leer el archivo según su extensión
				if nombre_archivo.endswith('.csv'):
					historia = pd.read_csv(archivo, delimiter=';', encoding='latin-1')
				elif nombre_archivo.endswith('.xlsx'):
					historia = pd.read_excel(archivo, engine='openpyxl')
				elif nombre_archivo.endswith('.xls'):
					historia = pd.read_excel(archivo, engine='xlrd')
				else:
					# Intentar como CSV por defecto
					historia = pd.read_csv(archivo, delimiter=';', encoding='latin-1')
				
				# Normalizar columnas
				historia.columns = historia.columns.str.strip().str.lower()
				
				# Extraer código del estudiante del nombre del archivo
				codigo_estudiante = None
				match = re.search(r'Historia-Academica[_-]?(\d+)', nombre_archivo, re.IGNORECASE)
				if match:
					codigo_estudiante = match.group(1)
				else:
					# Usar el nombre del archivo sin extensión
					codigo_estudiante = os.path.splitext(nombre_archivo)[0]
				
				# Ejecutar comparación
				resultado = comparar_estudiante(historia, pensum, config=config, programa_id=programa_id)
				
				# Reorganizar resultado para que 'estudiante' aparezca primero
				resultado_ordenado = {}
				if codigo_estudiante:
					resultado_ordenado['estudiante'] = codigo_estudiante
				resultado_ordenado.update(resultado)
				
				resultados.append(resultado_ordenado)
				
			except Exception as e:
				logger.error(f"Error procesando archivo {archivo.name}: {str(e)}", exc_info=True)
				archivos_con_error.append({
					'archivo': archivo.name,
					'error': str(e)
				})
		
		# Calcular estadísticas
		total_estudiantes = len(resultados)
		elegibles = sum(1 for r in resultados if r['estado'] == 1)
		no_elegibles = total_estudiantes - elegibles
		
		respuesta = {
			'total_estudiantes': total_estudiantes,
			'elegibles': elegibles,
			'no_elegibles': no_elegibles,
			'resultados': resultados
		}
		
		# Incluir errores si los hubo
		if archivos_con_error:
			respuesta['archivos_con_error'] = archivos_con_error
			respuesta['warning'] = f'{len(archivos_con_error)} archivo(s) no pudieron ser procesados'
		
		return Response(respuesta, status=status.HTTP_200_OK)
		
	except Exception as e:
		logger.error(f"Exception en verificación masiva: {type(e).__name__}: {str(e)}", exc_info=True)
		return Response({
			'error': 'Error al procesar la solicitud masiva',
			'details': str(e)
		}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
