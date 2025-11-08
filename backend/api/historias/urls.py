from django.urls import path
from .controllers.comparadorController import (
    verificar_elegibilidad_estudiante,
    verificar_elegibilidad_masiva,
    obtener_estadisticas_elegibilidad
)

urlpatterns = [
    path("verificar/estudiante/", verificar_elegibilidad_estudiante, name="verificar_elegibilidad_estudiante"),
    path("verificar/masiva/", verificar_elegibilidad_masiva, name="verificar_elegibilidad_masiva"),
    path("estadisticas/", obtener_estadisticas_elegibilidad, name="estadisticas_elegibilidad"),
]

