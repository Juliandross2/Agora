from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from api.oferta_electiva.services.service_oferta_electiva import OfertaElectivaService
from api.oferta_electiva.serializers.serializer_oferta_electiva import (
    OfertaElectivaCreateUpdateSerializer,
    OfertaElectivaResponseSerializer
)
import json
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter

class OfertaElectivaController:
    def __init__(self):
        self.service = OfertaElectivaService()

oferta_electiva_controller = OfertaElectivaController()

@extend_schema(
    tags=['OfertaElectiva - Público'],
    summary="Listar ofertas electivas activas",
    description="Devuelve la lista de ofertas electivas activas ordenadas por id descendente.",
    responses={
        200: OpenApiResponse(
            description="Lista de ofertas activas",
            examples=[
                OpenApiExample(
                    "Success",
                    value=[
                        {"oferta_electiva_id": 1, "electiva_id": 5, "periodo": 202401, "es_activa": True}
                    ]
                )
            ]
        ),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def listar_ofertas_activas(request):
    try:
        success, response = oferta_electiva_controller.service.listar_ofertas_activas()
        if success:
            return Response(response, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['OfertaElectiva - Público'],
    summary="Obtener oferta electiva activa por ID",
    parameters=[OpenApiParameter(name='oferta_id', type=int, location=OpenApiParameter.PATH, description='ID de la oferta electiva', required=True)],
    responses={
        200: OpenApiResponse(description="Oferta encontrada", examples=[OpenApiExample("Success", value={"oferta_electiva_id": 1, "electiva_id": 5, "periodo": 202401, "es_activa": True})]),
        404: OpenApiResponse(description="Oferta no encontrada o inactiva", examples=[OpenApiExample("Not Found", value={"error": "Oferta no encontrada o inactiva"})]),
        400: OpenApiResponse(description="ID inválido", examples=[OpenApiExample("Invalid ID", value={"error": "ID inválido"})]),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def obtener_oferta(request, oferta_id):
    try:
        success, response = oferta_electiva_controller.service.obtener_oferta_activa(oferta_id)
        if success:
            return Response(response, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['OfertaElectiva - Admin'],
    summary="Crear nueva oferta electiva",
    description="Crea una nueva oferta electiva. request: { electiva_id: int, periodo: int, es_activa?: bool }",
    request=OfertaElectivaCreateUpdateSerializer,
    responses={
        201: OpenApiResponse(description="Oferta creada exitosamente", examples=[OpenApiExample("Created", value={"oferta_electiva_id": 10, "electiva_id": 5, "periodo": 202401, "es_activa": True})]),
        400: OpenApiResponse(description="Datos inválidos", examples=[OpenApiExample("Validation Error", value={"error": "Datos inválidos", "details": {"periodo": ["This field is required."]}})]),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])  # cambiar a IsAuthenticated si aplica
def crear_oferta(request):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.data

        serializer = OfertaElectivaCreateUpdateSerializer(data=data)
        if not serializer.is_valid():
            return Response({'error': 'Datos inválidos', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        success, response = oferta_electiva_controller.service.crear_oferta(serializer.validated_data)
        if success:
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except json.JSONDecodeError:
        return Response({'error': 'JSON inválido'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['OfertaElectiva - Admin'],
    summary="Actualizar oferta electiva",
    description="Actualiza una oferta electiva activa. Enviar solo campos a actualizar.",
    parameters=[OpenApiParameter(name='oferta_id', type=int, location=OpenApiParameter.PATH, required=True)],
    request=OfertaElectivaCreateUpdateSerializer,
    responses={
        200: OpenApiResponse(description="Oferta actualizada", examples=[OpenApiExample("Success", value={"oferta_electiva_id": 1, "electiva_id": 5, "periodo": 202402, "es_activa": True})]),
        400: OpenApiResponse(description="Datos inválidos", examples=[OpenApiExample("Validation Error", value={"error": "Datos inválidos", "details": {"periodo": ["A valid integer is required."]}})]),
        404: OpenApiResponse(description="Oferta no encontrada o inactiva", examples=[OpenApiExample("Not Found", value={"error": "Oferta no encontrada o inactiva"})]),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
@api_view(['PUT'])
@permission_classes([AllowAny])
def actualizar_oferta(request, oferta_id):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.data

        success, response = oferta_electiva_controller.service.actualizar_oferta(oferta_id, data)
        if success:
            return Response(response, status=status.HTTP_200_OK)
        # service returns dict with error/details
        return Response(response, status=status.HTTP_400_BAD_REQUEST if 'details' in response or 'error' in response else status.HTTP_200_OK)
    except json.JSONDecodeError:
        return Response({'error': 'JSON inválido'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['OfertaElectiva - Admin'],
    summary="Eliminar (desactivar) oferta electiva",
    description="Marca como inactiva una oferta electiva activa (soft delete).",
    parameters=[OpenApiParameter(name='oferta_id', type=int, location=OpenApiParameter.PATH, required=True)],
    responses={
        200: OpenApiResponse(description="Oferta marcada como inactiva", examples=[OpenApiExample("Success", value={"message": "Oferta marcada como inactiva"})]),
        404: OpenApiResponse(description="Oferta no encontrada o ya inactiva", examples=[OpenApiExample("Not Found", value={"error": "Oferta no encontrada o ya inactiva"})]),
        500: OpenApiResponse(description="Error interno del servidor")
    }
)
@api_view(['DELETE'])
@permission_classes([AllowAny])
def eliminar_oferta(request, oferta_id):
    try:
        success, response = oferta_electiva_controller.service.eliminar_oferta(oferta_id)
        if success:
            return Response(response, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': 'Error interno del servidor', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    tags=['OfertaElectiva - Público'],
    summary="Endpoint de prueba para oferta electiva",
    responses={200: OpenApiResponse(description="Estado OK", examples=[OpenApiExample("Test", value={"message": "API OfertaElectiva funcionando correctamente", "status": "OK"})])}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def test_oferta_electiva_connection(request):
    return Response({'message': 'API OfertaElectiva funcionando correctamente', 'status': 'OK'}, status=status.HTTP_200_OK)
