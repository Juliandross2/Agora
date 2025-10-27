from django.urls import path
from api.electiva.controllers import controller_electiva

urlpatterns = [
    # Endpoint de prueba
    path('test/', controller_electiva.test_electiva_connection, name='test-electiva-connection'),
    
    # CRUD básico
    path('', controller_electiva.listar_electivas, name='listar-electivas'),
    path('<int:electiva_id>/', controller_electiva.obtener_electiva, name='obtener-electiva'),
    path('crear/', controller_electiva.crear_electiva, name='crear-electiva'),
    path('<int:electiva_id>/actualizar/', controller_electiva.actualizar_electiva, name='actualizar-electiva'),
    path('<int:electiva_id>/eliminar/', controller_electiva.eliminar_electiva, name='eliminar-electiva'),
    
    # Filtros y búsquedas
    path('activas/', controller_electiva.listar_electivas_activas, name='listar-electivas-activas'),
    path('programa/<int:programa_id>/', controller_electiva.obtener_electivas_por_programa, name='obtener-electivas-programa'),
    path('buscar/', controller_electiva.buscar_electivas, name='buscar-electivas'),
]

