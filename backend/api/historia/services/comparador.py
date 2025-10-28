import pandas as pd

def comparar_con_pensum(pensum_path, historias):
    pensum = pd.read_excel(pensum_path)
    pensum.columns = pensum.columns.str.strip().str.lower()
    pensum_hasta_7 = pensum[pensum['semestre'] <= 7]
    materias_requeridas = pensum_hasta_7['materia'].str.strip().str.lower().tolist()

    resultados = []

    for historia in historias:
        nombre_estudiante = historia['archivo'].iloc[0].replace('.csv', '')
        historia['definitiva'] = pd.to_numeric(historia['definitiva'], errors='coerce')
        historia = historia.dropna(subset=['materia'])
        historia['materia'] = historia['materia'].str.strip().str.lower()

        aprobadas = historia[historia['definitiva'] >= 3]['materia'].unique().tolist()
        faltantes = [m for m in materias_requeridas if m not in aprobadas]
        semestre_max = historia['semestre'].max()

        if semestre_max >= 7 and not faltantes:
            estado = 1
            mensaje = "Elegible para electivas"
        elif semestre_max < 7:
            estado = 0
            mensaje = f"No elegible (solo cursó hasta {semestre_max}° semestre)"
        else:
            estado = 0
            mensaje = "No elegible (faltan materias hasta 7° semestre)"

        resultados.append({
            "estudiante": nombre_estudiante,
            "semestre_maximo_cursado": int(semestre_max),
            "estado": estado,
            "mensaje": mensaje,
            "materias_aprobadas": aprobadas,
            "materias_faltantes": faltantes
        })

    return resultados
