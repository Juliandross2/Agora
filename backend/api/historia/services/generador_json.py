import json
import os

def guardar_resultados_json(resultados, salida_path):
    os.makedirs(os.path.dirname(salida_path), exist_ok=True)
    with open(salida_path, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)
    print(f"✅ Resultados guardados en {salida_path}")
