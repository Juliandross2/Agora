from django.db import models

# Cargamos los modelos para que django los reconozca
from api.electiva.models.electiva import Electiva
from api.configuracion.models.configuracion_elegibilidad import ConfiguracionElegibilidad
from api.materia.models.materia import Materia
from api.oferta_electiva.models.oferta_electiva import OfertaElectiva
from api.pensum.models.pensum import Pensum
from api.programa.models.programa import Programa
from api.usuario.models.usuario import Usuario
