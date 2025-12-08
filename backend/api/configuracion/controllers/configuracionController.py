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
			'required': False,
			'schema': {'type': 'integer'},
			'description': 'ID del programa. Si no se proporciona, retorna error'
		}
	],
	responses={
		200: OpenApiResponse(
			description="Configuración obtenida exitosamente",
			examples=[
				OpenApiExample(
					'Ejemplo de respuesta',
					value={
						"configuracion_id": 1,
						"programa_id": 1,
						"programa_nombre": "Ingeniería de Sistemas",
						"nota_aprobatoria": 3.0,
						"semestre_limite_electivas": 7,
						"es_activo": True
					}
				)
			]
		),
		404: OpenApiResponse(description="No se encontró configuración")
	},
	tags=['configuracion-elegibilidad'],
	summary="Obtener configuración activa"
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
			'nota_aprobatoria': serializers.FloatField(required=False, help_text='Nota mínima para aprobar. Por defecto: 3.0'),
			'semestre_limite_electivas': serializers.IntegerField(required=False, help_text='Semestre límite para exigir materias aprobadas. Por defecto: 7'),
		}
	),
	responses={
		201: OpenApiResponse(description="Configuración creada exitosamente"),
		400: OpenApiResponse(description="Datos inválidos"),
		500: OpenApiResponse(description="Error interno del servidor")
	},
	tags=['configuracion-elegibilidad'],
	summary="Crear/actualizar configuración"
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
			'description': 'ID del programa. Si no se proporciona, lista todas las configuraciones'
		}
	],
	responses={
		200: OpenApiResponse(description="Lista de configuraciones"),
	},
	tags=['configuracion-elegibilidad'],
	summary="Listar configuraciones"
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
					'Ejemplo de respuesta',
					value={
						"configuracion_id": 5,
						"programa_id": 1,
						"programa_nombre": "Ingeniería de Sistemas",
						"nota_aprobatoria": 3.0,
						"semestre_limite_electivas": 7,
						"es_activo": True,
						"fecha_creacion": "2025-11-27T19:00:00",
						"fecha_actualizacion": "2025-11-27T19:00:00"
					}
				)
			]
		),
		404: OpenApiResponse(description="Configuración no encontrada")
	},
	tags=['configuracion-elegibilidad'],
	summary="Obtener configuración por ID"
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
	responses={
		200: OpenApiResponse(
			description="Configuración activa del programa obtenida exitosamente",
			examples=[
				OpenApiExample(
					'Ejemplo de respuesta',
					value={
						"configuracion_id": 5,
						"programa_id": 1,
						"programa_nombre": "Ingeniería de Sistemas",
						"nota_aprobatoria": 3.0,
						"semestre_limite_electivas": 7,
						"es_activo": True,
						"fecha_creacion": "2025-11-27T19:00:00",
						"fecha_actualizacion": "2025-11-27T19:00:00"
					}
				)
			]
		),
		404: OpenApiResponse(description="No se encontró configuración activa para el programa")
	},
	tags=['configuracion-elegibilidad'],
	summary="Obtener configuración activa por programa"
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
			'nota_aprobatoria': serializers.FloatField(required=False, help_text='Nota mínima para aprobar'),
			'semestre_limite_electivas': serializers.IntegerField(required=False, help_text='Semestre límite'),
		}
	),
	responses={
		200: OpenApiResponse(description="Configuración actualizada exitosamente"),
		404: OpenApiResponse(description="Configuración no encontrada"),
		400: OpenApiResponse(description="Datos inválidos")
	},
	tags=['configuracion-elegibilidad'],
	summary="Actualizar configuración existente"
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
			'es_activo': serializers.BooleanField(required=True, help_text='True para activar, False para desactivar')
		}
	),
	responses={
		200: OpenApiResponse(description="Estado de configuración actualizado"),
		404: OpenApiResponse(description="Configuración no encontrada"),
		400: OpenApiResponse(description="Datos inválidos")
	},
	tags=['configuracion-elegibilidad'],
	summary="Activar/Desactivar configuración"
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
	responses={
		204: OpenApiResponse(description="Configuración eliminada exitosamente"),
		404: OpenApiResponse(description="Configuración no encontrada"),
		400: OpenApiResponse(description="No se puede eliminar la configuración activa")
	},
	tags=['configuracion-elegibilidad'],
	summary="Eliminar configuración"
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

