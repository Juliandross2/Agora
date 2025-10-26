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

from api.oferta_electiva.controllers.controller_oferta_electiva import actualizar_oferta, crear_oferta, eliminar_oferta, listar_ofertas_activas, obtener_oferta
from api.usuario.controllers.controller_usuario import login, register, profile, test_connection
from api.programa.controllers.controller_programa import (
    listar_programas, obtener_programa, crear_programa, actualizar_programa,
    eliminar_programa, listar_programas_activos, buscar_programas, test_programa_connection
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
]   
