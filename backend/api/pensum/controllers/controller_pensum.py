from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from api.pensum.services.services_pensum import PensumService
from api.pensum.serializers.serializer_pensum import PensumCreateUpdateSerializer
import json
from drf_spectacular.utils import extend_schema, OpenApiResponse

class PensumController:
    def __init__(self):
        self.service = PensumService()

pensum_controller = PensumController()

@extend_schema(tags=['Pensum - Público'], summary="Listar todos los pensums")
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

@extend_schema(tags=['Pensum - Público'], summary="Obtener pensum por ID")
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
    request=PensumCreateUpdateSerializer,
    responses={201: OpenApiResponse(description="Pensum creado")}
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
    request=PensumCreateUpdateSerializer
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

@extend_schema(tags=['Pensum - Admin'], summary="Eliminar pensum")
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

@extend_schema(tags=['Pensum - Público'], summary="Listar pensums activos")
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

@extend_schema(tags=['Pensum - Público'], summary="Buscar pensums por programa (query ?programa_id=)")
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
    
    
@extend_schema(tags=['Pensum - Público'], summary="Obtener estadísticas detalladas del pensum")
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

@extend_schema(tags=['Pensum - Público'], summary="Obtener resumen de créditos por programa")
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