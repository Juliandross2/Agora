from django.urls import path
from .controllers.configuracionController import (
    obtener_configuracion_activa,
    crear_configuracion,
    listar_configuraciones,
    obtener_configuracion_por_id,
    obtener_configuracion_por_programa,
    actualizar_configuracion,
    toggle_configuracion,
    eliminar_configuracion
)

urlpatterns = [
    # Obtener configuración activa (query param)
    path("", obtener_configuracion_activa, name="obtener_configuracion_activa"),
    
    # CRUD de configuraciones
    path("crear/", crear_configuracion, name="crear_configuracion"),
    path("listar/", listar_configuraciones, name="listar_configuraciones"),
    path("programa/<int:programa_id>/", obtener_configuracion_por_programa, name="obtener_configuracion_por_programa"),
    path("<int:id>/", obtener_configuracion_por_id, name="obtener_configuracion_por_id"),
    path("<int:id>/actualizar/", actualizar_configuracion, name="actualizar_configuracion"),
    path("<int:id>/toggle/", toggle_configuracion, name="toggle_configuracion"),
    path("<int:id>/eliminar/", eliminar_configuracion, name="eliminar_configuracion"),
]

