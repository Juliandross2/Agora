from django.urls import path
from .controllers.comparadorController import (
    verificar_elegibilidad_estudiante,
    verificar_elegibilidad_masiva
)

urlpatterns = [
    path("verificar/estudiante/", verificar_elegibilidad_estudiante, name="verificar_elegibilidad_estudiante"),
    path("verificar/masiva/", verificar_elegibilidad_masiva, name="verificar_elegibilidad_masiva"),
]
