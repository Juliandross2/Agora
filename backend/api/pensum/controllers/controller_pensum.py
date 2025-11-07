from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from api.pensum.services.services_pensum import PensumService
from api.pensum.serializers.serializer_pensum import PensumCreateUpdateSerializer, PensumSerializer, PensumDetailSerializer
import json
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter

class PensumController:
    def __init__(self):
        self.service = PensumService()

pensum_controller = PensumController()

@extend_schema(
    tags=['Pensum - Público'], 
    summary="Listar pensums por programa",
    description="Obtiene todos los pensums (activos e inactivos) de un programa específico ordenados por año de creación descendente.",
    parameters=[
        OpenApiParameter(
            name='programa_id',
            type=int,
            location=OpenApiParameter.PATH,
            description='ID del programa para filtrar los pensums',
            required=True
        )
    ],
    responses={
        200: OpenApiResponse(
            description="Lista de pensums obtenida exitosamente",
            examples=[
                OpenApiExample(
                    "Success Example",
                    value={
                        "programa_id": 1,
                        "programa_nombre": "Ingeniería de Sistemas",
                        "pensums": [
                            {
                                "pensum_id": 1,
                                "programa_id": 1,
                                "anio_creacion": 2024,
                                "es_activo": True,
                                "creditos_obligatorios_totales": 120,
                                "total_materias_obligatorias": 45,
                                "total_materias_electivas": 8
                            }
                        ],
                        "total": 1
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="Error en los parámetros o programa no encontrado",
            examples=[
                OpenApiExample(
                    "Invalid programa_id",
                    value={"error": "programa_id inválido"}
                ),
                OpenApiExample(
                    "Programa not found",
                    value={"error": "Programa no encontrado"}
                )
            ]
        ),
        500: OpenApiResponse(
            description="Error interno del servidor",
            examples=[
                OpenApiExample(
                    "Server Error",
                    value={"error": "Error interno del servidor", "details": "Database connection failed"}
                )
            ]
        )
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def listar_pensums_por_programa(request, programa_id):
    """Listar todos los pensums de un programa específico"""
    try:
        success, response = pensum_controller.service.obtener_pensums_por_programa(programa_id)
        if success:
            return Response(response, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['Pensum - Público'], 
    summary="Listar pensums activos por programa",
    description="Obtiene solo los pensums activos de un programa específico. Debería retornar máximo un pensum por la lógica de negocio.",
    parameters=[
        OpenApiParameter(
            name='programa_id',
            type=int,
            location=OpenApiParameter.PATH,
            description='ID del programa para filtrar los pensums activos',
            required=True
        )
    ],
    responses={
        200: OpenApiResponse(
            description="Lista de pensums activos obtenida exitosamente",
            examples=[
                OpenApiExample(
                    "Success Example",
                    value={
                        "programa_id": 1,
                        "programa_nombre": "Ingeniería de Sistemas",
                        "pensums_activos": [
                            {
                                "pensum_id": 1,
                                "programa_id": 1,
                                "anio_creacion": 2024,
                                "es_activo": True,
                                "creditos_obligatorios_totales": 120,
                                "total_materias_obligatorias": 45,
                                "total_materias_electivas": 8
                            }
                        ],
                        "total": 1
                    }
                ),
                OpenApiExample(
                    "No Active Pensums",
                    value={
                        "programa_id": 1,
                        "programa_nombre": "Ingeniería de Sistemas",
                        "pensums_activos": [],
                        "total": 0
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="Error en los parámetros o programa no encontrado",
            examples=[
                OpenApiExample(
                    "Invalid programa_id",
                    value={"error": "programa_id inválido"}
                ),
                OpenApiExample(
                    "Programa not found",
                    value={"error": "Programa no encontrado"}
                )
            ]
        ),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def listar_pensums_activos_por_programa(request, programa_id):
    """Listar pensums activos de un programa específico"""
    try:
        success, response = pensum_controller.service.obtener_pensums_activos_por_programa(programa_id)
        if success:
            return Response(response, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['Pensum - Público'], 
    summary="Obtener pensum actual de un programa",
    description="Obtiene el pensum actualmente vigente (activo) de un programa específico. Solo debe haber uno por programa.",
    parameters=[
        OpenApiParameter(
            name='programa_id',
            type=int,
            location=OpenApiParameter.PATH,
            description='ID del programa para obtener su pensum actual',
            required=True
        )
    ],
    responses={
        200: OpenApiResponse(
            description="Pensum actual obtenido exitosamente",
            examples=[
                OpenApiExample(
                    "Success Example",
                    value={
                        "programa_id": 1,
                        "programa_nombre": "Ingeniería de Sistemas",
                        "pensum_actual": {
                            "pensum_id": 1,
                            "programa_id": 1,
                            "programa_nombre": "Ingeniería de Sistemas",
                            "anio_creacion": 2024,
                            "es_activo": True,
                            "creditos_obligatorios_totales": 120,
                            "total_materias_obligatorias": 45,
                            "total_materias_electivas": 8
                        }
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="Error en los parámetros o programa no encontrado",
            examples=[
                OpenApiExample(
                    "Invalid programa_id",
                    value={"error": "programa_id inválido"}
                ),
                OpenApiExample(
                    "Programa not found",
                    value={"error": "Programa no encontrado"}
                )
            ]
        ),
        404: OpenApiResponse(
            description="No hay pensum activo para el programa",
            examples=[
                OpenApiExample(
                    "No Active Pensum",
                    value={"error": "No hay pensum activo para el programa Ingeniería de Sistemas"}
                )
            ]
        ),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def obtener_pensum_actual_por_programa(request, programa_id):
    """Obtener el pensum actual (activo) de un programa específico"""
    try:
        success, response = pensum_controller.service.obtener_pensum_actual_por_programa(programa_id)
        if success:
            return Response(response, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['Pensum - Público'], 
    summary="[DEPRECATED] Listar todos los pensums",
    description="⚠️ DEPRECATED: Use listar_pensums_por_programa en su lugar. Este endpoint lista todos los pensums sin filtrar por programa.",
    responses={
        200: OpenApiResponse(
            description="Lista de todos los pensums",
            examples=[
                OpenApiExample(
                    "Success Example",
                    value=[
                        {
                            "pensum_id": 1,
                            "programa_id": 1,
                            "anio_creacion": 2024,
                            "es_activo": True,
                            "creditos_obligatorios_totales": 120,
                            "total_materias_obligatorias": 45,
                            "total_materias_electivas": 8
                        }
                    ]
                )
            ]
        ),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def listar_pensums(request):
    try:
        success, response = pensum_controller.service.obtener_todos_pensums()
        if success:
            return Response(response, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['Pensum - Público'], 
    summary="Obtener pensum por ID",
    description="Obtiene los detalles completos de un pensum específico usando su ID único.",
    parameters=[
        OpenApiParameter(
            name='pensum_id',
            type=int,
            location=OpenApiParameter.PATH,
            description='ID único del pensum a obtener',
            required=True
        )
    ],
    responses={
        200: OpenApiResponse(
            description="Pensum obtenido exitosamente",
            examples=[
                OpenApiExample(
                    "Success Example",
                    value={
                        "pensum_id": 1,
                        "programa_id": 1,
                        "programa_nombre": "Ingeniería de Sistemas",
                        "anio_creacion": 2024,
                        "es_activo": True,
                        "creditos_obligatorios_totales": 120,
                        "total_materias_obligatorias": 45,
                        "total_materias_electivas": 8
                    }
                )
            ]
        ),
        404: OpenApiResponse(
            description="Pensum no encontrado",
            examples=[
                OpenApiExample(
                    "Not Found",
                    value={"error": "Pensum no encontrado"}
                )
            ]
        ),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def obtener_pensum(request, pensum_id):
    try:
        success, response = pensum_controller.service.obtener_pensum_por_id(pensum_id)
        if success:
            return Response(response, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['Pensum - Admin'],
    summary="Crear nuevo pensum",
    description="Crea un nuevo pensum para un programa. Si se marca como activo, automáticamente desactiva otros pensums del mismo programa (solo puede haber uno activo por programa).",
    request=PensumCreateUpdateSerializer,
    examples=[
        OpenApiExample(
            "Create Active Pensum",
            value={
                "programa_id": 1,
                "anio_creacion": 2024,
                "es_activo": True
            }
        ),
        OpenApiExample(
            "Create Inactive Pensum",
            value={
                "programa_id": 1,
                "anio_creacion": 2023,
                "es_activo": False
            }
        ),
        OpenApiExample(
            "Minimal Request",
            value={
                "programa_id": 1
            }
        )
    ],
    responses={
        201: OpenApiResponse(
            description="Pensum creado exitosamente",
            examples=[
                OpenApiExample(
                    "Success Example",
                    value={
                        "message": "Pensum creado exitosamente para el programa Ingeniería de Sistemas",
                        "pensum": {
                            "pensum_id": 1,
                            "programa_id": 1,
                            "programa_nombre": "Ingeniería de Sistemas",
                            "anio_creacion": 2024,
                            "es_activo": True,
                            "creditos_obligatorios_totales": 0,
                            "total_materias_obligatorias": 0,
                            "total_materias_electivas": 0
                        }
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="Error en los datos enviados",
            examples=[
                OpenApiExample(
                    "Validation Error",
                    value={
                        "error": "Datos inválidos",
                        "details": {
                            "programa_id": "This field is required."
                        }
                    }
                ),
                OpenApiExample(
                    "Program Not Found",
                    value={"error": "Programa inválido o no encontrado"}
                ),
                OpenApiExample(
                    "Already Active Pensum",
                    value={
                        "error": "Ya existe un pensum activo para el programa Ingeniería de Sistemas. Solo puede haber un pensum activo por programa.",
                        "suggestion": "Desactive el pensum actual antes de crear uno nuevo activo, o cree este pensum como inactivo."
                    }
                )
            ]
        ),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])  # cambiar a IsAuthenticated si aplica
def crear_pensum(request):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.data

        serializer = PensumCreateUpdateSerializer(data=data)
        if not serializer.is_valid():
            return Response({'error': 'Datos inválidos', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        success, response = pensum_controller.service.crear_pensum(serializer.validated_data)
        if success:
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except json.JSONDecodeError:
        return Response({'error': 'JSON inválido'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['Pensum - Admin'],
    summary="Actualizar pensum existente",
    description="Actualiza un pensum existente. Si se cambia a activo, automáticamente desactiva otros pensums del mismo programa.",
    parameters=[
        OpenApiParameter(
            name='pensum_id',
            type=int,
            location=OpenApiParameter.PATH,
            description='ID del pensum a actualizar',
            required=True
        )
    ],
    request=PensumCreateUpdateSerializer,
    examples=[
        OpenApiExample(
            "Update to Active",
            value={
                "es_activo": True
            }
        ),
        OpenApiExample(
            "Update Year",
            value={
                "anio_creacion": 2025
            }
        ),
        OpenApiExample(
            "Full Update",
            value={
                "programa_id": 2,
                "anio_creacion": 2024,
                "es_activo": True
            }
        )
    ],
    responses={
        200: OpenApiResponse(
            description="Pensum actualizado exitosamente",
            examples=[
                OpenApiExample(
                    "Success Example",
                    value={
                        "message": "Pensum actualizado exitosamente",
                        "pensum": {
                            "pensum_id": 1,
                            "programa_id": 1,
                            "programa_nombre": "Ingeniería de Sistemas",
                            "anio_creacion": 2024,
                            "es_activo": True,
                            "creditos_obligatorios_totales": 120,
                            "total_materias_obligatorias": 45,
                            "total_materias_electivas": 8
                        }
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="Error en los datos o conflicto de pensum activo",
            examples=[
                OpenApiExample(
                    "Validation Error",
                    value={
                        "error": "Datos inválidos",
                        "details": {
                            "programa_id": "Programa no encontrado"
                        }
                    }
                ),
                OpenApiExample(
                    "Active Pensum Conflict",
                    value={
                        "error": "Ya existe un pensum activo para este programa. Solo puede haber un pensum activo por programa.",
                        "suggestion": "Desactive el pensum actual antes de activar este."
                    }
                ),
                OpenApiExample(
                    "Pensum Not Found",
                    value={"error": "Pensum no encontrado"}
                )
            ]
        ),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
@api_view(['PUT'])
@permission_classes([AllowAny])
def actualizar_pensum(request, pensum_id):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.data

        serializer = PensumCreateUpdateSerializer(data=data, partial=True)
        if not serializer.is_valid():
            return Response({'error': 'Datos inválidos', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        success, response = pensum_controller.service.actualizar_pensum(pensum_id, serializer.validated_data)
        if success:
            return Response(response, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except json.JSONDecodeError:
        return Response({'error': 'JSON inválido'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['Pensum - Admin'], 
    summary="Eliminar pensum",
    description="Elimina (desactiva) un pensum existente. Es una eliminación lógica, el pensum se marca como inactivo.",
    parameters=[
        OpenApiParameter(
            name='pensum_id',
            type=int,
            location=OpenApiParameter.PATH,
            description='ID del pensum a eliminar',
            required=True
        )
    ],
    responses={
        200: OpenApiResponse(
            description="Pensum eliminado exitosamente",
            examples=[
                OpenApiExample(
                    "Success Example",
                    value={"message": "Pensum eliminado (desactivado) correctamente"}
                )
            ]
        ),
        400: OpenApiResponse(
            description="Pensum no encontrado",
            examples=[
                OpenApiExample(
                    "Not Found",
                    value={"error": "Pensum no encontrado"}
                )
            ]
        ),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
@api_view(['DELETE'])
@permission_classes([AllowAny])
def eliminar_pensum(request, pensum_id):
    try:
        success, response = pensum_controller.service.eliminar_pensum(pensum_id)
        if success:
            return Response(response, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['Pensum - Público'], 
    summary="[DEPRECATED] Listar pensums activos",
    description="⚠️ DEPRECATED: Use listar_pensums_activos_por_programa en su lugar. Lista todos los pensums activos sin filtrar por programa.",
    responses={
        200: OpenApiResponse(
            description="Lista de pensums activos",
            examples=[
                OpenApiExample(
                    "Success Example",
                    value=[
                        {
                            "pensum_id": 1,
                            "programa_id": 1,
                            "anio_creacion": 2024,
                            "es_activo": True,
                            "creditos_obligatorios_totales": 120,
                            "total_materias_obligatorias": 45,
                            "total_materias_electivas": 8
                        }
                    ]
                )
            ]
        ),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def listar_pensums_activos(request):
    try:
        success, response = pensum_controller.service.obtener_pensums_activos()
        if success:
            return Response(response, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['Pensum - Público'], 
    summary="Buscar pensums por programa",
    description="Busca pensums filtrados por programa usando query parameter. Alternativa al endpoint por path parameter.",
    parameters=[
        OpenApiParameter(
            name='programa_id',
            type=int,
            location=OpenApiParameter.QUERY,
            description='ID del programa para filtrar los pensums',
            required=True,
            examples=[
                OpenApiExample(
                    "Search by program",
                    value=1
                )
            ]
        )
    ],
    responses={
        200: OpenApiResponse(
            description="Pensums encontrados exitosamente",
            examples=[
                OpenApiExample(
                    "Success Example",
                    value={
                        "programa_id": 1,
                        "programa_nombre": "Ingeniería de Sistemas",
                        "pensums": [
                            {
                                "pensum_id": 1,
                                "programa_id": 1,
                                "anio_creacion": 2024,
                                "es_activo": True,
                                "creditos_obligatorios_totales": 120,
                                "total_materias_obligatorias": 45,
                                "total_materias_electivas": 8
                            }
                        ],
                        "total": 1
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="Parámetros faltantes o inválidos",
            examples=[
                OpenApiExample(
                    "Missing Parameter",
                    value={"error": "Parámetro \"programa_id\" requerido"}
                ),
                OpenApiExample(
                    "Invalid programa_id",
                    value={"error": "programa_id inválido"}
                ),
                OpenApiExample(
                    "Programa not found",
                    value={"error": "Programa no encontrado"}
                )
            ]
        ),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def buscar_pensums(request):
    try:
        programa_id = request.GET.get('programa_id', '').strip()
        if not programa_id:
            return Response({'error': 'Parámetro "programa_id" requerido'}, status=status.HTTP_400_BAD_REQUEST)

        success, response = pensum_controller.service.buscar_pensums_por_programa(programa_id)
        if success:
            return Response(response, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['Pensum - Público'], 
    summary="Obtener estadísticas detalladas del pensum",
    description="Obtiene estadísticas completas del pensum incluyendo créditos totales, materias obligatorias, electivas y información del programa.",
    parameters=[
        OpenApiParameter(
            name='pensum_id',
            type=int,
            location=OpenApiParameter.PATH,
            description='ID del pensum para obtener estadísticas',
            required=True
        )
    ],
    responses={
        200: OpenApiResponse(
            description="Estadísticas obtenidas exitosamente",
            examples=[
                OpenApiExample(
                    "Success Example",
                    value={
                        "pensum_id": 1,
                        "programa_id": 1,
                        "programa_nombre": "Ingeniería de Sistemas",
                        "anio_creacion": 2024,
                        "creditos_obligatorios_totales": 120,
                        "total_materias_obligatorias": 45,
                        "total_materias_electivas": 8,
                        "total_creditos_electivas": 24,
                        "total_materias": 53,
                        "es_activo": True
                    }
                )
            ]
        ),
        404: OpenApiResponse(
            description="Pensum no encontrado",
            examples=[
                OpenApiExample(
                    "Not Found",
                    value={"error": "Pensum no encontrado"}
                )
            ]
        ),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def obtener_estadisticas_pensum(request, pensum_id):
    try:
        success, response = pensum_controller.service.obtener_estadisticas_pensum(pensum_id)
        if success:
            return Response(response, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['Pensum - Público'], 
    summary="Obtener resumen de créditos por programa",
    description="Obtiene un resumen de créditos y materias de todos los pensums de un programa específico, útil para comparaciones entre versiones.",
    parameters=[
        OpenApiParameter(
            name='programa_id',
            type=int,
            location=OpenApiParameter.PATH,
            description='ID del programa para obtener el resumen de créditos',
            required=True
        )
    ],
    responses={
        200: OpenApiResponse(
            description="Resumen de créditos obtenido exitosamente",
            examples=[
                OpenApiExample(
                    "Success Example",
                    value={
                        "programa_id": 1,
                        "programa_nombre": "Ingeniería de Sistemas",
                        "resumen_pensums": [
                            {
                                "pensum_id": 1,
                                "anio_creacion": 2024,
                                "creditos_obligatorios": 120,
                                "creditos_electivas": 24,
                                "materias_obligatorias": 45,
                                "materias_electivas": 8,
                                "total_materias": 53,
                                "es_activo": True
                            },
                            {
                                "pensum_id": 2,
                                "anio_creacion": 2023,
                                "creditos_obligatorios": 115,
                                "creditos_electivas": 20,
                                "materias_obligatorias": 43,
                                "materias_electivas": 7,
                                "total_materias": 50,
                                "es_activo": False
                            }
                        ],
                        "total_pensums": 2
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="Error en los parámetros o programa no encontrado",
            examples=[
                OpenApiExample(
                    "Invalid programa_id",
                    value={"error": "programa_id inválido"}
                ),
                OpenApiExample(
                    "Programa not found",
                    value={"error": "Programa no encontrado"}
                )
            ]
        ),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def obtener_resumen_creditos(request, programa_id):
    try:
        success, response = pensum_controller.service.obtener_resumen_creditos_por_programa(programa_id)
        if success:
            return Response(response, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)