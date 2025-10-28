from historias.lector_csv import leer_historias
from historias.comparador import comparar_con_pensum
from historias.generador_json import guardar_resultados_json
from historias.vistas import mostrar_resumen

# Rutas
ruta_pensum = 'data/Pensum_PIS.xlsx'
carpeta_historias = 'data/historias/'
ruta_salida = 'resultados/resultados_elegibilidad.json'

#Leer historias académicas
historias = leer_historias(carpeta_historias)

# Comparar con pensum
resultados = comparar_con_pensum(ruta_pensum, historias)

# Guardar resultados
guardar_resultados_json(resultados, ruta_salida)

# Mostrar resumen
mostrar_resumen(resultados)
