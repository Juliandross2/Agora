from django.urls import path
from .views import verificar_elegibilidad

urlpatterns = [
    path("verificar/", verificar_elegibilidad, name="verificar_elegibilidad"),
]

