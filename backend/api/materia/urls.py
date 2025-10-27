from django.urls import path
from api.materia.controllers import controller_materia

urlpatterns = [
    # Endpoint de prueba
    path('test/', controller_materia.test_materia_connection, name='test-materia-connection'),
    
    # CRUD básico
    path('', controller_materia.listar_materias, name='listar-materias'),
    path('<int:materia_id>/', controller_materia.obtener_materia, name='obtener-materia'),
    path('crear/', controller_materia.crear_materia, name='crear-materia'),
    path('<int:materia_id>/actualizar/', controller_materia.actualizar_materia, name='actualizar-materia'),
    path('<int:materia_id>/eliminar/', controller_materia.eliminar_materia, name='eliminar-materia'),
    
    # Filtros y búsquedas
    path('activas/', controller_materia.listar_materias_activas, name='listar-materias-activas'),
    path('pensum/<int:pensum_id>/', controller_materia.obtener_materias_por_pensum, name='obtener-materias-pensum'),
    path('semestre/<int:semestre>/', controller_materia.obtener_materias_por_semestre, name='obtener-materias-semestre'),
    path('buscar/', controller_materia.buscar_materias, name='buscar-materias'),
    path('obligatorias/', controller_materia.listar_materias_obligatorias, name='listar-materias-obligatorias'),
]

