from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
import json

from api.oferta_electiva.services.service_oferta_electiva import OfertaElectivaService

service = OfertaElectivaService()

@extend_schema(
    request=None,
    responses={201: OpenApiResponse(description="Oferta creada"), 400: OpenApiResponse(description="Datos inválidos")},
    tags=['oferta-electiva']
)
@api_view(['POST'])
def crear_oferta(request):
	"""
	Crear nueva oferta electiva
	"""
	try:
		data = json.loads(request.body) if request.content_type == 'application/json' else request.data
		success, resp = service.crear_oferta(data)
		if success:
			return Response(resp, status=status.HTTP_201_CREATED)
		return Response(resp, status=status.HTTP_400_BAD_REQUEST)
	except json.JSONDecodeError:
		return Response({'error': 'JSON inválido'}, status=status.HTTP_400_BAD_REQUEST)
	except Exception as e:
		return Response({'error': 'Error interno', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(responses={200: OpenApiResponse(description="Lista de ofertas activas")}, tags=['oferta-electiva'])
@api_view(['GET'])
def listar_ofertas_activas(request):
	try:
		success, resp = service.listar_ofertas_activas()
		return Response(resp, status=status.HTTP_200_OK)
	except Exception as e:
		return Response({'error': 'Error interno', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(responses={200: OpenApiResponse(description="Oferta activa encontrada"), 404: OpenApiResponse(description="No encontrada")}, tags=['oferta-electiva'])
@api_view(['GET'])
def obtener_oferta(request, oferta_id: int):
	try:
		success, resp = service.obtener_oferta_activa(oferta_id)
		if success:
			return Response(resp, status=status.HTTP_200_OK)
		return Response(resp, status=status.HTTP_404_NOT_FOUND)
	except Exception as e:
		return Response({'error': 'Error interno', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(responses={200: OpenApiResponse(description="Oferta actualizada"), 400: OpenApiResponse(description="Datos inválidos"), 404: OpenApiResponse(description="No encontrada")}, tags=['oferta-electiva'])
@api_view(['PUT', 'PATCH'])
def actualizar_oferta(request, oferta_id: int):
	try:
		data = json.loads(request.body) if request.content_type == 'application/json' else request.data
		success, resp = service.actualizar_oferta(oferta_id, data)
		if success:
			return Response(resp, status=status.HTTP_200_OK)
		# distinguir entre not found y bad request por la estructura del resp
		if 'error' in resp and ('no encontrada' in resp['error'].lower() or 'inactiva' in resp['error'].lower()):
			return Response(resp, status=status.HTTP_404_NOT_FOUND)
		return Response(resp, status=status.HTTP_400_BAD_REQUEST)
	except json.JSONDecodeError:
		return Response({'error': 'JSON inválido'}, status=status.HTTP_400_BAD_REQUEST)
	except Exception as e:
		return Response({'error': 'Error interno', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(responses={200: OpenApiResponse(description="Oferta marcada como inactiva"), 404: OpenApiResponse(description="No encontrada")}, tags=['oferta-electiva'])
@api_view(['DELETE'])
def eliminar_oferta(request, oferta_id: int):
	try:
		success, resp = service.eliminar_oferta(oferta_id)
		if success:
			return Response(resp, status=status.HTTP_200_OK)
		return Response(resp, status=status.HTTP_404_NOT_FOUND)
	except Exception as e:
		return Response({'error': 'Error interno', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
