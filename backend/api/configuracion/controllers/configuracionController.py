from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, inline_serializer
from rest_framework import serializers
import logging

from api.configuracion.models.configuracion_elegibilidad import ConfiguracionElegibilidad
from api.historias.config.config import CONFIG

# Configurar logger
logger = logging.getLogger(__name__)


def guardar_configuracion_en_bd(config_dict, programa_id):
    """
    Guarda una configuración en la base de datos.
    Desactiva configuraciones anteriores del mismo programa antes de crear la nueva.
    
    Args:
        config_dict: Diccionario con la configuración a guardar
        programa_id: ID del programa (requerido)
    
    Returns:
        ConfiguracionElegibilidad: La configuración guardada
        
    Raises:
        ValueError: Si el programa_id no es válido o no existe
    """
    try:
        # Validar que se proporcione programa_id
        if not programa_id:
            raise ValueError("programa_id es requerido")
            
        # Obtener el programa
        from api.programa.models.programa import Programa
        try:
            programa = Programa.objects.get(programa_id=programa_id)
        except Programa.DoesNotExist:
            raise ValueError(f"Programa con ID {programa_id} no existe")
        
        # Desactivar configuraciones anteriores del mismo programa
        configs_anteriores = ConfiguracionElegibilidad.objects.filter(
            programa_id=programa_id,
            es_activo=True
        )
        if configs_anteriores.exists():
            configs_anteriores.update(es_activo=False)
        
        # Completar configuración con valores por defecto si faltan
        config_completa = {
            'nota_aprobatoria': CONFIG['nota_aprobatoria'],
            'semestre_limite_electivas': CONFIG['semestre_limite_electivas'],
        }
        config_completa.update(config_dict)
        
        # Crear nueva configuración
        nueva_config = ConfiguracionElegibilidad(
            programa_id=programa,
            nota_aprobatoria=config_completa.get('nota_aprobatoria', CONFIG['nota_aprobatoria']),
            semestre_limite_electivas=config_completa.get('semestre_limite_electivas', CONFIG['semestre_limite_electivas']),
            es_activo=True
        )
        nueva_config.save()
        return nueva_config
        
    except Exception as e:
        logger.error(f"Error al guardar configuración en BD: {e}", exc_info=True)
        raise


def obtener_configuracion(programa_id):
    """
    Obtiene la configuración de elegibilidad desde la base de datos.
    
    Orden de prioridad:
    1. Configuración activa para el programa específico
    2. Si no existe, lanza una excepción
    
    Args:
        programa_id: ID del programa (requerido)
    
    Returns:
        Diccionario con la configuración a usar
        
    Raises:
        ValueError: Si no existe configuración en BD para el programa
    """
    try:
        config_db = ConfiguracionElegibilidad.get_config_activa(programa_id=programa_id)
        if config_db:
            return config_db.to_dict()
        
        # Si no se encuentra configuración, lanzar error
        raise ValueError(
            f'No existe configuración de elegibilidad para el programa {programa_id}. '
            f'Debe crear una usando POST /api/configuracion/crear/'
        )
    except ConfiguracionElegibilidad.DoesNotExist:
        raise ValueError(
            f'No existe configuración de elegibilidad para el programa {programa_id}. '
            f'Debe crear una usando POST /api/configuracion/crear/'
        )


# ==================== ENDPOINTS ====================

@extend_schema(
	request=None,
	parameters=[
		{
			'name': 'programa_id',
			'in': 'query',
			'required': True,
			'schema': {'type': 'integer'},
			'description': 'ID del programa (requerido)'
		}
	],
	responses={
		200: OpenApiResponse(
			description="Configuración obtenida exitosamente",
			examples=[
				OpenApiExample(
					'Éxito - Configuración encontrada',
					value={
						"configuracion_id": 20,
						"programa_id": 1,
						"programa_nombre": "Ingeniería Sistemas",
						"nota_aprobatoria": 3.0,
						"semestre_limite_electivas": 8,
						"es_activo": True,
						"fecha_creacion": "2025-11-27T19:56:24.796694",
						"fecha_actualizacion": "2025-11-27T19:56:24.796763"
					},
					status_codes=['200']
				)
			]
		),
		400: OpenApiResponse(
			description="Parámetro inválido",
			examples=[
				OpenApiExample(
					'Error - programa_id inválido',
					value={
						"error": "programa_id inválido",
						"details": "El programa_id debe ser un número entero"
					},
					status_codes=['400']
				)
			]
		),
		404: OpenApiResponse(
			description="Configuración no encontrada",
			examples=[
				OpenApiExample(
					'Error - No existe configuración',
					value={
						"error": "Configuración no encontrada",
						"details": "No existe configuración activa para el programa 1",
						"accion": "Debe crear una configuración usando POST /api/configuracion/crear/"
					},
					status_codes=['404']
				)
			]
		)
	},
	tags=['configuracion-elegibilidad'],
	summary="Obtener configuración activa por programa",
	description="Obtiene la configuración de elegibilidad activa para un programa específico.\n\n**Parámetros a enviar:**\n- `programa_id` (query, requerido): ID del programa (número entero)\n\n**Ejemplo de solicitud:**\n```\nGET /api/configuracion/obtener/?programa_id=1\n```\n\n**Respuesta exitosa (200):**\nRetorna un objeto JSON con la configuración activa incluyendo ID, programa, nota aprobatoria, semestre límite y fechas.\n\n**Errores posibles:**\n- 400: programa_id no es un número entero\n- 404: No existe configuración activa para el programa"
)
@api_view(['GET'])
def obtener_configuracion_activa(request):
	"""
	Obtiene la configuración de elegibilidad activa para un programa específico.
	"""
	try:
		programa_id = request.GET.get('programa_id')
		if programa_id:
			try:
				programa_id = int(programa_id)
			except (ValueError, TypeError):
				return Response({
					'error': 'programa_id inválido',
					'details': 'El programa_id debe ser un número entero'
				}, status=status.HTTP_400_BAD_REQUEST)
		
		config = ConfiguracionElegibilidad.get_config_activa(programa_id=programa_id)
		
		if not config:
			tipo = f"el programa {programa_id}" if programa_id else "configuración global"
			return Response({
				'error': 'Configuración no encontrada',
				'details': f'No existe configuración activa para {tipo}',
				'accion': 'Debe crear una configuración usando POST /api/configuracion/crear/'
			}, status=status.HTTP_404_NOT_FOUND)
		
		# Construir respuesta con información completa
		respuesta = {
			'configuracion_id': config.configuracion_id,
			'programa_id': config.programa_id.programa_id,
			'programa_nombre': config.programa_id.nombre_programa,
			'nota_aprobatoria': float(config.nota_aprobatoria),
			'semestre_limite_electivas': config.semestre_limite_electivas,
			'es_activo': config.es_activo,
			'fecha_creacion': config.fecha_creacion.isoformat(),
			'fecha_actualizacion': config.fecha_actualizacion.isoformat()
		}
		
		return Response(respuesta, status=status.HTTP_200_OK)
		
	except Exception as e:
		logger.error(f"Error al obtener configuración: {e}", exc_info=True)
		return Response({
			'error': 'Error al obtener configuración',
			'details': str(e)
		}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
	request=inline_serializer(
		name='CrearConfiguracionRequest',
		fields={
			'programa_id': serializers.IntegerField(required=True, help_text='ID del programa (requerido)'),
			'nota_aprobatoria': serializers.FloatField(required=False, help_text='Nota mínima para aprobar (0-5). Por defecto: 3.0'),
			'semestre_limite_electivas': serializers.IntegerField(required=False, help_text='Semestre límite para exigir todas las materias aprobadas. Por defecto: 7'),
		}
	),
	responses={
		201: OpenApiResponse(
			description="Configuración creada exitosamente",
			examples=[
				OpenApiExample(
					'Éxito - Configuración creada',
					value={
						"mensaje": "Configuración creada exitosamente",
						"configuracion_id": 21,
						"programa_id": 1,
						"programa_nombre": "Ingeniería Sistemas",
						"configuracion": {
							"nota_aprobatoria": 3.0,
							"semestre_limite_electivas": 8
						}
					},
					status_codes=['201']
				)
			]
		),
		400: OpenApiResponse(
			description="Datos inválidos",
			examples=[
				OpenApiExample(
					'Error - programa_id faltante',
					value={
						"error": "programa_id es requerido",
						"details": "Debe proporcionar el ID del programa para crear la configuración"
					},
					status_codes=['400']
				)
			]
		),
		404: OpenApiResponse(
			description="Programa no encontrado",
			examples=[
				OpenApiExample(
					'Error - Programa no existe',
					value={
						"error": "Programa no encontrado",
						"details": "No existe un programa con ID 999"
					},
					status_codes=['404']
				)
			]
		),
		500: OpenApiResponse(description="Error interno del servidor")
	},
	tags=['configuracion-elegibilidad'],
	summary="Crear nueva configuración",
	description="Crea una nueva configuración de elegibilidad para un programa.\nSi ya existe una configuración activa para el programa, la desactiva automáticamente y crea la nueva.\n\n**Body (JSON) a enviar:**\n```json\n{\n  \"programa_id\": 1,\n  \"nota_aprobatoria\": 3.0,\n  \"semestre_limite_electivas\": 8\n}\n```\n\n**Campos requeridos:**\n- `programa_id` (integer): ID del programa\n\n**Campos opcionales:**\n- `nota_aprobatoria` (float): Valor entre 0 y 5 (default: 3.0)\n- `semestre_limite_electivas` (integer): Número de semestre (default: 7)\n\n**Respuesta exitosa (201):**\nRetorna objeto con mensaje de confirmación, IDs y datos de la configuración creada.\n\n**Errores posibles:**\n- 400: Datos incompletos o inválidos\n- 404: El programa no existe"
)
@api_view(['POST'])
def crear_configuracion(request):
	"""
	Crea o actualiza la configuración de elegibilidad para un programa.
	Si ya existe una configuración activa para el programa, la desactiva y crea una nueva.
	"""
	try:
		# Obtener programa_id (requerido)
		programa_id = request.data.get('programa_id')
		if not programa_id:
			return Response({
				'error': 'programa_id es requerido',
				'details': 'Debe proporcionar el ID del programa para crear la configuración'
			}, status=status.HTTP_400_BAD_REQUEST)
		
		if programa_id:
			try:
				programa_id = int(programa_id)
				# Validar que el programa existe
				from api.programa.models.programa import Programa
				if not Programa.objects.filter(programa_id=programa_id).exists():
					return Response({
						'error': 'Programa no encontrado',
						'details': f'No existe un programa con ID {programa_id}'
					}, status=status.HTTP_404_NOT_FOUND)
			except (ValueError, TypeError):
				return Response({
					'error': 'programa_id inválido',
					'details': 'El programa_id debe ser un número entero'
				}, status=status.HTTP_400_BAD_REQUEST)
		
		# Construir diccionario de configuración
		config_data = {}
		if 'nota_aprobatoria' in request.data:
			config_data['nota_aprobatoria'] = request.data['nota_aprobatoria']
		if 'semestre_limite_electivas' in request.data:
			config_data['semestre_limite_electivas'] = request.data['semestre_limite_electivas']
		
		# Guardar configuración
		nueva_config = guardar_configuracion_en_bd(config_data, programa_id=programa_id)
		
		# Construir respuesta
		respuesta = {
			'mensaje': 'Configuración creada exitosamente',
			'configuracion_id': nueva_config.configuracion_id,
			'programa_id': nueva_config.programa_id.programa_id,
			'programa_nombre': nueva_config.programa_id.nombre_programa,
			'configuracion': nueva_config.to_dict()
		}
		
		return Response(respuesta, status=status.HTTP_201_CREATED)
		
	except Exception as e:
		logger.error(f"Error al crear configuración: {e}", exc_info=True)
		return Response({
			'error': 'Error al crear configuración',
			'details': str(e)
		}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
	request=None,
	parameters=[
		{
			'name': 'programa_id',
			'in': 'query',
			'required': False,
			'schema': {'type': 'integer'},
			'description': 'ID del programa para filtrar. Si no se proporciona, lista todas'
		}
	],
	responses={
		200: OpenApiResponse(
			description="Lista de configuraciones obtenida",
			examples=[
				OpenApiExample(
					'Éxito - Lista de configuraciones',
					value={
						"total": 2,
						"configuraciones": [
							{
								"configuracion_id": 20,
								"programa_id": 1,
								"programa_nombre": "Ingeniería Sistemas",
								"nota_aprobatoria": 3.0,
								"semestre_limite_electivas": 8,
								"es_activo": True,
								"fecha_creacion": "2025-11-27T19:56:24"
							},
							{
								"configuracion_id": 19,
								"programa_id": 1,
								"programa_nombre": "Ingeniería Sistemas",
								"nota_aprobatoria": 3.0,
								"semestre_limite_electivas": 7,
								"es_activo": False,
								"fecha_creacion": "2025-11-27T19:55:07"
							}
						]
					},
					status_codes=['200']
				)
			]
		),
		400: OpenApiResponse(
			description="Parámetro inválido",
			examples=[
				OpenApiExample(
					'Error - programa_id no es número',
					value={
						"error": "programa_id inválido"
					},
					status_codes=['400']
				)
			]
		)
	},
	tags=['configuracion-elegibilidad'],
	summary="Listar todas las configuraciones",
	description="Lista las configuraciones de elegibilidad con opción de filtrar por programa.\n\n**Parámetros a enviar:**\n- `programa_id` (query, opcional): Filtra solo configuraciones de ese programa\n\n**Ejemplos de solicitud:**\n```\nGET /api/configuracion/listar/                    # Lista todas\nGET /api/configuracion/listar/?programa_id=1      # Solo del programa 1\n```\n\n**Respuesta exitosa (200):**\nRetorna objeto con `total` (cantidad) y array `configuraciones` con todos los registros ordenados por fecha más reciente.\n\n**Errores posibles:**\n- 400: El programa_id no es un número entero"
)
@api_view(['GET'])
def listar_configuraciones(request):
	"""
	Lista todas las configuraciones de elegibilidad, filtradas opcionalmente por programa.
	"""
	try:
		programa_id = request.GET.get('programa_id')
		
		if programa_id:
			try:
				programa_id = int(programa_id)
				configs = ConfiguracionElegibilidad.objects.filter(programa_id=programa_id).order_by('-fecha_creacion')
			except (ValueError, TypeError):
				return Response({
					'error': 'programa_id inválido'
				}, status=status.HTTP_400_BAD_REQUEST)
		else:
			configs = ConfiguracionElegibilidad.objects.all().order_by('-fecha_creacion')
		
		resultados = []
		for config in configs:
			resultados.append({
				'configuracion_id': config.configuracion_id,
				'programa_id': config.programa_id.programa_id,
				'programa_nombre': config.programa_id.nombre_programa,
				'nota_aprobatoria': float(config.nota_aprobatoria),
				'semestre_limite_electivas': config.semestre_limite_electivas,
				'es_activo': config.es_activo,
				'fecha_creacion': config.fecha_creacion.isoformat(),
			})
		
		return Response({
			'total': len(resultados),
			'configuraciones': resultados
		}, status=status.HTTP_200_OK)
		
	except Exception as e:
		logger.error(f"Error al listar configuraciones: {e}", exc_info=True)
		return Response({
			'error': 'Error al listar configuraciones',
			'details': str(e)
		}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
	request=None,
	parameters=[
		{
			'name': 'id',
			'in': 'path',
			'required': True,
			'schema': {'type': 'integer'},
			'description': 'ID de la configuración'
		}
	],
	responses={
		200: OpenApiResponse(
			description="Configuración obtenida exitosamente",
			examples=[
				OpenApiExample(
					'Éxito - Configuración encontrada',
					value={
						"configuracion_id": 5,
						"programa_id": 1,
						"programa_nombre": "Ingeniería de Sistemas",
						"nota_aprobatoria": 3.0,
						"semestre_limite_electivas": 7,
						"es_activo": True,
						"fecha_creacion": "2025-11-27T19:00:00",
						"fecha_actualizacion": "2025-11-27T19:00:00"
					},
					status_codes=['200']
				)
			]
		),
		404: OpenApiResponse(
			description="Configuración no encontrada",
			examples=[
				OpenApiExample(
					'Error - ID no existe',
					value={
						"error": "Configuración no encontrada",
						"details": "No existe configuración con ID 999"
					},
					status_codes=['404']
				)
			]
		)
	},
	tags=['configuracion-elegibilidad'],
	summary="Obtener configuración por ID",
	description="Obtiene los detalles completos de una configuración específica usando su ID.\n\n**Parámetro a enviar:**\n- `id` (path, requerido): ID de la configuración\n\n**Ejemplo de solicitud:**\n```\nGET /api/configuracion/20/\n```\n\n**Respuesta exitosa (200):**\nRetorna objeto JSON con todos los detalles de la configuración incluyendo fechas de creación y actualización.\n\n**Errores posibles:**\n- 404: No existe configuración con ese ID"
)
@api_view(['GET'])
def obtener_configuracion_por_id(request, id):
	"""
	Obtiene los detalles de una configuración específica por su ID.
	"""
	try:
		config = ConfiguracionElegibilidad.objects.get(configuracion_id=id)
		
		respuesta = {
			'configuracion_id': config.configuracion_id,
			'programa_id': config.programa_id.programa_id,
			'programa_nombre': config.programa_id.nombre_programa,
			'nota_aprobatoria': float(config.nota_aprobatoria),
			'semestre_limite_electivas': config.semestre_limite_electivas,
			'es_activo': config.es_activo,
			'fecha_creacion': config.fecha_creacion.isoformat(),
			'fecha_actualizacion': config.fecha_actualizacion.isoformat()
		}
		
		return Response(respuesta, status=status.HTTP_200_OK)
		
	except ConfiguracionElegibilidad.DoesNotExist:
		return Response({
			'error': 'Configuración no encontrada',
			'details': f'No existe configuración con ID {id}'
		}, status=status.HTTP_404_NOT_FOUND)
	except Exception as e:
		logger.error(f"Error al obtener configuración {id}: {e}", exc_info=True)
		return Response({
			'error': 'Error al obtener configuración',
			'details': str(e)
		}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
	request=None,
	parameters=[
		{
			'name': 'programa_id',
			'in': 'path',
			'required': True,
			'schema': {'type': 'integer'},
			'description': 'ID del programa'
		}
	],
	responses={
		200: OpenApiResponse(
			description="Configuración activa del programa obtenida",
			examples=[
				OpenApiExample(
					'Éxito - Configuración activa encontrada',
					value={
						"configuracion_id": 5,
						"programa_id": 1,
						"programa_nombre": "Ingeniería de Sistemas",
						"nota_aprobatoria": 3.0,
						"semestre_limite_electivas": 7,
						"es_activo": True,
						"fecha_creacion": "2025-11-27T19:00:00",
						"fecha_actualizacion": "2025-11-27T19:00:00"
					},
					status_codes=['200']
				)
			]
		),
		404: OpenApiResponse(
			description="Programa no encontrado o sin configuración",
			examples=[
				OpenApiExample(
					'Error - Programa no existe',
					value={
						"error": "Programa no encontrado",
						"details": "No existe un programa con ID 999"
					},
					status_codes=['404']
				),
				OpenApiExample(
					'Error - Sin configuración activa',
					value={
						"error": "Configuración no encontrada",
						"details": "No existe configuración activa para el programa 1",
						"accion": "Debe crear una usando POST /api/configuracion/crear/"
					},
					status_codes=['404']
				)
			]
		)
	},
	tags=['configuracion-elegibilidad'],
	summary="Obtener configuración activa de un programa",
	description="Obtiene la configuración activa de un programa específico por su ID.\n\n**Parámetro a enviar:**\n- `programa_id` (path, requerido): ID del programa\n\n**Ejemplo de solicitud:**\n```\nGET /api/configuracion/programa/1/\n```\n\n**Respuesta exitosa (200):**\nRetorna la configuración activa del programa con todos sus detalles.\n\n**Errores posibles:**\n- 404: El programa no existe o no tiene configuración activa"
)
@api_view(['GET'])
def obtener_configuracion_por_programa(request, programa_id):
	"""
	Obtiene la configuración activa de un programa específico.
	"""
	try:
		# Validar que el programa existe
		from api.programa.models.programa import Programa
		if not Programa.objects.filter(programa_id=programa_id).exists():
			return Response({
				'error': 'Programa no encontrado',
				'details': f'No existe un programa con ID {programa_id}'
			}, status=status.HTTP_404_NOT_FOUND)
		
		# Obtener configuración activa
		config = ConfiguracionElegibilidad.get_config_activa(programa_id=programa_id)
		
		if not config:
			return Response({
				'error': 'Configuración no encontrada',
				'details': f'No existe configuración activa para el programa {programa_id}',
				'accion': 'Debe crear una usando POST /api/configuracion/crear/'
			}, status=status.HTTP_404_NOT_FOUND)
		
		# Construir respuesta
		respuesta = {
			'configuracion_id': config.configuracion_id,
			'programa_id': config.programa_id.programa_id,
			'programa_nombre': config.programa_id.nombre_programa,
			'nota_aprobatoria': float(config.nota_aprobatoria),
			'semestre_limite_electivas': config.semestre_limite_electivas,
			'es_activo': config.es_activo,
			'fecha_creacion': config.fecha_creacion.isoformat(),
			'fecha_actualizacion': config.fecha_actualizacion.isoformat()
		}
		
		return Response(respuesta, status=status.HTTP_200_OK)
		
	except Exception as e:
		logger.error(f"Error al obtener configuración del programa {programa_id}: {e}", exc_info=True)
		return Response({
			'error': 'Error al obtener configuración',
			'details': str(e)
		}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
	request=inline_serializer(
		name='ActualizarConfiguracionRequest',
		fields={
			'nota_aprobatoria': serializers.FloatField(required=False, help_text='Nota mínima para aprobar (0-5)'),
			'semestre_limite_electivas': serializers.IntegerField(required=False, help_text='Semestre límite'),
		}
	),
	responses={
		200: OpenApiResponse(
			description="Configuración actualizada exitosamente",
			examples=[
				OpenApiExample(
					'Éxito - Configuración actualizada',
					value={
						"mensaje": "Configuración actualizada exitosamente",
						"configuracion_id": 20,
						"configuracion": {
							"programa_id": 1,
							"programa_nombre": "Ingeniería Sistemas",
							"nota_aprobatoria": 3.5,
							"semestre_limite_electivas": 8,
							"es_activo": True
						}
					},
					status_codes=['200']
				)
			]
		),
		404: OpenApiResponse(
			description="Configuración no encontrada",
			examples=[
				OpenApiExample(
					'Error - ID no existe',
					value={
						"error": "Configuración no encontrada",
						"details": "No existe configuración con ID 999"
					},
					status_codes=['404']
				)
			]
		),
		400: OpenApiResponse(description="Datos inválidos")
	},
	tags=['configuracion-elegibilidad'],
	summary="Actualizar configuración",
	description="Actualiza los campos de una configuración existente sin crear una nueva.\n\n**Body (JSON) a enviar:**\n```json\n{\n  \"nota_aprobatoria\": 3.5,\n  \"semestre_limite_electivas\": 8\n}\n```\n\n**Campos que se pueden actualizar:**\n- `nota_aprobatoria` (float, opcional): Valor entre 0 y 5\n- `semestre_limite_electivas` (integer, opcional): Número de semestre\n\n**Métodos soportados:** PUT o PATCH\n\n**Ejemplo de solicitud:**\n```\nPUT /api/configuracion/20/actualizar/\n```\n\n**Respuesta exitosa (200):**\nRetorna mensaje de confirmación con los datos actualizados.\n\n**Errores posibles:**\n- 400: Datos inválidos\n- 404: La configuración no existe"
)
@api_view(['PUT', 'PATCH'])
def actualizar_configuracion(request, id):
	"""
	Actualiza una configuración existente sin crear una nueva.
	"""
	try:
		config = ConfiguracionElegibilidad.objects.get(configuracion_id=id)
		
		# Actualizar solo los campos proporcionados
		if 'nota_aprobatoria' in request.data:
			config.nota_aprobatoria = request.data['nota_aprobatoria']
		if 'semestre_limite_electivas' in request.data:
			config.semestre_limite_electivas = request.data['semestre_limite_electivas']
		
		config.save()
		
		return Response({
			'mensaje': 'Configuración actualizada exitosamente',
			'configuracion_id': config.configuracion_id,
			'configuracion': {
				'programa_id': config.programa_id.programa_id,
				'programa_nombre': config.programa_id.nombre_programa,
				'nota_aprobatoria': float(config.nota_aprobatoria),
				'semestre_limite_electivas': config.semestre_limite_electivas,
				'es_activo': config.es_activo
			}
		}, status=status.HTTP_200_OK)
		
	except ConfiguracionElegibilidad.DoesNotExist:
		return Response({
			'error': 'Configuración no encontrada',
			'details': f'No existe configuración con ID {id}'
		}, status=status.HTTP_404_NOT_FOUND)
	except Exception as e:
		logger.error(f"Error al actualizar configuración {id}: {e}", exc_info=True)
		return Response({
			'error': 'Error al actualizar configuración',
			'details': str(e)
		}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
	request=inline_serializer(
		name='ToggleConfiguracionRequest',
		fields={
			'es_activo': serializers.BooleanField(required=True, help_text='true para activar, false para desactivar')
		}
	),
	responses={
		200: OpenApiResponse(
			description="Estado de configuración actualizado",
			examples=[
				OpenApiExample(
					'Éxito - Configuración activada',
					value={
						"mensaje": "Configuración activada exitosamente",
						"configuracion_id": 20,
						"programa_id": 1,
						"programa_nombre": "Ingeniería Sistemas",
						"es_activo": True
					},
					status_codes=['200']
				),
				OpenApiExample(
					'Éxito - Configuración desactivada',
					value={
						"mensaje": "Configuración desactivada exitosamente",
						"configuracion_id": 19,
						"programa_id": 1,
						"programa_nombre": "Ingeniería Sistemas",
						"es_activo": False
					},
					status_codes=['200']
				)
			]
		),
		404: OpenApiResponse(
			description="Configuración no encontrada",
			examples=[
				OpenApiExample(
					'Error - ID no existe',
					value={
						"error": "Configuración no encontrada",
						"details": "No existe configuración con ID 999"
					},
					status_codes=['404']
				)
			]
		),
		400: OpenApiResponse(
			description="Datos inválidos o operación no permitida",
			examples=[
				OpenApiExample(
					'Error - Campo faltante',
					value={
						"error": "Campo requerido",
						"details": "Debe proporcionar el campo \"es_activo\" (true/false)"
					},
					status_codes=['400']
				)
			]
		)
	},
	tags=['configuracion-elegibilidad'],
	summary="Activar o desactivar configuración",
	description="Activa o desactiva una configuración específica.\nAl activar una configuración, automáticamente desactiva otras del mismo programa.\n\n**Body (JSON) a enviar:**\n```json\n{\n  \"es_activo\": true\n}\n```\n\n**Campos requeridos:**\n- `es_activo` (boolean): true para activar, false para desactivar\n\n**Ejemplo de solicitud:**\n```\nPOST /api/configuracion/20/toggle/\n```\n\n**Respuesta exitosa (200):**\nRetorna mensaje de confirmación con el nuevo estado de la configuración.\n\n**Comportamiento especial:**\nSi activa una configuración, desactiva automáticamente las demás configuraciones activas del mismo programa.\n\n**Errores posibles:**\n- 400: Campo \"es_activo\" faltante o inválido\n- 404: La configuración no existe"
)
@api_view(['POST'])
def toggle_configuracion(request, id):
	"""
	Activa o desactiva una configuración específica.
	Al activar una configuración, desactiva automáticamente otras del mismo programa.
	"""
	try:
		config = ConfiguracionElegibilidad.objects.get(configuracion_id=id)
		
		es_activo = request.data.get('es_activo')
		if es_activo is None:
			return Response({
				'error': 'Campo requerido',
				'details': 'Debe proporcionar el campo "es_activo" (true/false)'
			}, status=status.HTTP_400_BAD_REQUEST)
		
		# Si se va a activar, desactivar otras del mismo programa
		if es_activo and not config.es_activo:
			# Desactivar otras configuraciones activas del mismo programa
			ConfiguracionElegibilidad.objects.filter(
				programa_id=config.programa_id,
				es_activo=True
			).exclude(configuracion_id=id).update(es_activo=False)
		
		# Actualizar estado
		config.es_activo = es_activo
		config.save()
		
		return Response({
			'mensaje': f'Configuración {"activada" if es_activo else "desactivada"} exitosamente',
			'configuracion_id': config.configuracion_id,
			'programa_id': config.programa_id.programa_id,
			'programa_nombre': config.programa_id.nombre_programa,
			'es_activo': config.es_activo
		}, status=status.HTTP_200_OK)
		
	except ConfiguracionElegibilidad.DoesNotExist:
		return Response({
			'error': 'Configuración no encontrada',
			'details': f'No existe configuración con ID {id}'
		}, status=status.HTTP_404_NOT_FOUND)
	except Exception as e:
		logger.error(f"Error al cambiar estado de configuración {id}: {e}", exc_info=True)
		return Response({
			'error': 'Error al cambiar estado de configuración',
			'details': str(e)
		}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
	request=None,
	parameters=[
		{
			'name': 'id',
			'in': 'path',
			'required': True,
			'schema': {'type': 'integer'},
			'description': 'ID de la configuración'
		}
	],
	responses={
		200: OpenApiResponse(
			description="Configuración eliminada exitosamente",
			examples=[
				OpenApiExample(
					'Éxito - Configuración eliminada',
					value={
						"mensaje": "Configuración eliminada exitosamente",
						"configuracion_id": 19,
						"programa": "Ingeniería Sistemas"
					},
					status_codes=['200']
				)
			]
		),
		404: OpenApiResponse(
			description="Configuración no encontrada",
			examples=[
				OpenApiExample(
					'Error - ID no existe',
					value={
						"error": "Configuración no encontrada",
						"details": "No existe configuración con ID 999"
					},
					status_codes=['404']
				)
			]
		),
		400: OpenApiResponse(
			description="No se puede eliminar configuración activa",
			examples=[
				OpenApiExample(
					'Error - Configuración activa',
					value={
						"error": "No se puede eliminar configuración activa",
						"details": "Primero desactive la configuración antes de eliminarla",
						"accion": "POST /api/configuracion/20/toggle/ con es_activo=false"
					},
					status_codes=['400']
				)
			]
		)
	},
	tags=['configuracion-elegibilidad'],
	summary="Eliminar configuración",
	description="Elimina una configuración de la base de datos.\n\n⚠️ **IMPORTANTE:** No se pueden eliminar configuraciones activas. Primero debe desactivarlas.\n\n**Parámetro a enviar:**\n- `id` (path, requerido): ID de la configuración\n\n**Ejemplo de solicitud:**\n```\nDELETE /api/configuracion/19/eliminar/\n```\n\n**Respuesta exitosa (200):**\nRetorna mensaje de confirmación con ID y nombre del programa.\n\n**Restricción importante:**\nNo se puede eliminar una configuración mientras esté activa. Debe desactivarla primero usando el endpoint de toggle.\n\n**Errores posibles:**\n- 400: La configuración está activa\n- 404: La configuración no existe"
)
@api_view(['DELETE'])
def eliminar_configuracion(request, id):
	"""
	Elimina una configuración de la base de datos.
	No permite eliminar configuraciones activas (deben desactivarse primero).
	"""
	try:
		config = ConfiguracionElegibilidad.objects.get(configuracion_id=id)
		
		# No permitir eliminar configuración activa
		if config.es_activo:
			return Response({
				'error': 'No se puede eliminar configuración activa',
				'details': 'Primero desactive la configuración antes de eliminarla',
				'accion': f'POST /api/configuracion/{id}/toggle/ con es_activo=false'
			}, status=status.HTTP_400_BAD_REQUEST)
		
		programa_nombre = config.programa_id.nombre_programa
		config.delete()
		
		return Response({
			'mensaje': 'Configuración eliminada exitosamente',
			'configuracion_id': id,
			'programa': programa_nombre
		}, status=status.HTTP_200_OK)
		
	except ConfiguracionElegibilidad.DoesNotExist:
		return Response({
			'error': 'Configuración no encontrada',
			'details': f'No existe configuración con ID {id}'
		}, status=status.HTTP_404_NOT_FOUND)
	except Exception as e:
		logger.error(f"Error al eliminar configuración {id}: {e}", exc_info=True)
		return Response({
			'error': 'Error al eliminar configuración',
			'details': str(e)
		}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

