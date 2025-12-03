"""
URL configuration for agora_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from api.oferta_electiva.controllers.controller_oferta_electiva import (
    actualizar_oferta, crear_oferta, eliminar_oferta, listar_ofertas_activas, obtener_oferta
)
from api.pensum.controllers.controller_pensum import (
    listar_pensums, listar_pensums_activos, obtener_pensum, crear_pensum,
    actualizar_pensum, eliminar_pensum, buscar_pensums,
    obtener_estadisticas_pensum, obtener_resumen_creditos,
    # Nuevos endpoints
    listar_pensums_por_programa, listar_pensums_activos_por_programa,
    obtener_pensum_actual_por_programa
)
from api.usuario.controllers.controller_usuario import (
    desactivar_mi_cuenta, listar_usuarios, listar_usuarios_activos, listar_usuarios_inactivos, login, register, profile, test_connection, activar_usuario
)
from api.programa.controllers.controller_programa import (
    listar_programas, obtener_programa, crear_programa, actualizar_programa,
    eliminar_programa, listar_programas_activos, buscar_programas, test_programa_connection
)
from api.materia.controllers.controller_materia import (
    listar_materias, obtener_materia, crear_materia, actualizar_materia,
    eliminar_materia, listar_materias_activas, obtener_materias_por_pensum,
    obtener_materias_por_semestre, buscar_materias, listar_materias_obligatorias, patch_materia,
    test_materia_connection
)
from api.electiva.controllers.controller_electiva import (
    listar_electivas, obtener_electiva, crear_electiva, actualizar_electiva,
    eliminar_electiva, listar_electivas_activas, obtener_electivas_por_programa,
    buscar_electivas, test_electiva_connection
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # documentación / esquema OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # usuario
    path('api/usuario/login/', login, name='usuario_login'),
    path('api/usuario/register/', register, name='usuario_register'),
    path('api/usuario/profile/', profile, name='usuario_profile'),
    path('api/usuario/test/', test_connection, name='usuario_test'),
    path('api/usuario/desactivar/', desactivar_mi_cuenta, name='usuario_desactivar'),
    path('api/usuario/<int:usuario_id>/activar/', activar_usuario, name='usuario_activar'),
    path('api/usuario-listar/', listar_usuarios, name='usuario_list_all'),
    path('api/usuario-listar/activos/', listar_usuarios_activos, name='usuario_list_activos'),
    path('api/usuario-listar/inactivos/', listar_usuarios_inactivos, name='usuario_list_inactivos'),

    # programa
    path('api/programa/', listar_programas, name='programa_list'),
    path('api/programa/<int:programa_id>/', obtener_programa, name='programa_detail'),
    path('api/programa/crear/', crear_programa, name='programa_create'),
    path('api/programa/<int:programa_id>/actualizar/', actualizar_programa, name='programa_update'),
    path('api/programa/<int:programa_id>/eliminar/', eliminar_programa, name='programa_delete'),
    path('api/programa/activos/', listar_programas_activos, name='programa_active_list'),
    path('api/programa/buscar/', buscar_programas, name='programa_search'),
    path('api/programa/test/', test_programa_connection, name='programa_test'),
    
    # oferta electiva
    path('api/oferta-electiva/', listar_ofertas_activas, name='oferta_electiva_list'),
    path('api/oferta-electiva/<int:oferta_id>/', obtener_oferta, name='oferta_electiva_detail'),
    path('api/oferta-electiva/crear/', crear_oferta, name='oferta_electiva_create'),
    path('api/oferta-electiva/<int:oferta_id>/actualizar/', actualizar_oferta, name='oferta_electiva_update'),
    path('api/oferta-electiva/<int:oferta_id>/eliminar/', eliminar_oferta, name='oferta_electiva_delete'),
    
    # pensum - Nuevos endpoints principales
    path('api/pensum/programa/<int:programa_id>/', listar_pensums_por_programa, name='pensum_list_by_programa'),
    path('api/pensum/programa/<int:programa_id>/activos/', listar_pensums_activos_por_programa, name='pensum_active_by_programa'),
    path('api/pensum/programa/<int:programa_id>/actual/', obtener_pensum_actual_por_programa, name='pensum_current_by_programa'),
    path('api/pensum/programa/<int:programa_id>/resumen-creditos/', obtener_resumen_creditos, name='pensum_resumen_creditos'),
    
    # pensum - Endpoints existentes (algunos marcados como deprecated)
    path('api/pensum/', listar_pensums, name='pensum_list_all'),  # DEPRECATED
    path('api/pensum/activos/', listar_pensums_activos, name='pensum_active_list'),  # DEPRECATED
    path('api/pensum/buscar/', buscar_pensums, name='pensum_search'),
    path('api/pensum/crear/', crear_pensum, name='pensum_create'),
    path('api/pensum/<int:pensum_id>/', obtener_pensum, name='pensum_detail'),
    path('api/pensum/<int:pensum_id>/actualizar/', actualizar_pensum, name='pensum_update'),
    path('api/pensum/<int:pensum_id>/eliminar/', eliminar_pensum, name='pensum_delete'),
    path('api/pensum/<int:pensum_id>/estadisticas/', obtener_estadisticas_pensum, name='pensum_estadisticas'),
    path('api/pensum/resumen-credito/<int:programa_id>/', obtener_resumen_creditos, name='pensum_resumen_creditos'),
    
    # historias / comparador
    path('api/historias/', include('api.historias.urls')),
    
    # configuración de elegibilidad
    path('api/configuracion/', include('api.configuracion.urls')),
    
    path("admin/", admin.site.urls),
    
    # materia
    path('api/materia/', listar_materias, name='materia_list'),
    path('api/materia/<int:materia_id>/', obtener_materia, name='materia_detail'),
    path('api/materia/crear/', crear_materia, name='materia_create'),
    path('api/materia/<int:materia_id>/actualizar/', actualizar_materia, name='materia_update'),
    path('api/materia/<int:materia_id>/patch/', patch_materia, name='materia_patch'),
    path('api/materia/<int:materia_id>/eliminar/', eliminar_materia, name='materia_delete'),
    path('api/materia/activas/', listar_materias_activas, name='materia_active_list'),
    path('api/materia/pensum/<int:pensum_id>/', obtener_materias_por_pensum, name='materia_by_pensum'),
    path('api/materia/semestre/<int:semestre>/', obtener_materias_por_semestre, name='materia_by_semestre'),
    path('api/materia/buscar/', buscar_materias, name='materia_search'),
    path('api/materia/obligatorias/', listar_materias_obligatorias, name='materia_obligatorias'),
    path('api/materia/test/', test_materia_connection, name='materia_test'),
    
    # electiva
    path('api/electiva/', listar_electivas, name='electiva_list'),
    path('api/electiva/<int:electiva_id>/', obtener_electiva, name='electiva_detail'),
    path('api/electiva/crear/', crear_electiva, name='electiva_create'),
    path('api/electiva/<int:electiva_id>/actualizar/', actualizar_electiva, name='electiva_update'),
    path('api/electiva/<int:electiva_id>/eliminar/', eliminar_electiva, name='electiva_delete'),
    path('api/electiva/activas/', listar_electivas_activas, name='electiva_active_list'),
    path('api/electiva/programa/<int:programa_id>/', obtener_electivas_por_programa, name='electiva_by_programa'),
    path('api/electiva/buscar/', buscar_electivas, name='electiva_search'),
    path('api/electiva/test/', test_electiva_connection, name='electiva_test'),
]
