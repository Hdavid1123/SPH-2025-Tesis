# initial_conditions/utils/io.py

import json
from pathlib import Path


def load_json(path: Path):
    """
    Lee un archivo JSON y retorna su contenido como dict.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo JSON: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_particle_data(file_path: Path, params: dict):
    """
    Carga datos de partículas desde un archivo de texto generado por exportadores.
    Retorna un diccionario con la misma estructura que esperan las funciones
    de summary.py.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de partículas: {file_path}")

    particles = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Se espera que cada línea sea "x y"
            try:
                x, y = map(float, line.split())
                particles.append((x, y))
            except ValueError:
                continue  # Ignorar líneas mal formateadas

    data = {
        "particles": particles,
        "spacing": params.get("espaciado"),
        "sections": params.get("sections", []),
        "holes": params.get("holes", []),
        "area": params.get("area"),
        "h": params.get("h"),
        "start_pos": params.get("start_pos"),
        "end_pos": params.get("end_pos"),
        "vertices": params.get("vertices")
    }

    return data
