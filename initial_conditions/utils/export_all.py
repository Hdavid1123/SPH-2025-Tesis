# initial_conditions/utils/export_all.py

from pathlib import Path
from typing import List, Dict
import matplotlib.pyplot as plt

# Exportadores individuales
from boundaries.export import export_boundary_particles
from fluid.export import export_fluid_particles

# Visualizadores
from boundaries.visualizer import visualize_boundary
from fluid.visualizer import visualize_fluid


def _parse_particle_file(path: Path) -> List[Dict]:
    """
    Parsea un archivo de partículas con formato:
    posx \t posy \t h \t type
    Devuelve lista de dicts: {"id": int, "position": [x,y], "h": h, "type": type}
    """
    parts = []
    if not path.exists():
        return parts

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Detectar si hay cabecera (línea con letras)
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if line == "":
            index += 1
            continue
        tokens = line.split()
        if any(tok.isalpha() for tok in tokens):
            index += 1
        break

    # Parsear líneas
    for line in lines[index:]:
        s = line.strip()
        if not s:
            continue
        toks = s.split()
        try:
            x = float(toks[0])
            y = float(toks[1]) if len(toks) > 1 else 0.0
            h = float(toks[2]) if len(toks) > 2 else 0.0
            ptype = int(float(toks[3])) if len(toks) > 3 else 0
        except Exception:
            continue

        parts.append({
            "id": len(parts),
            "position": [x, y],
            "h": h,
            "type": ptype
        })

    return parts


def _write_combined_file(boundary_file: Path, fluid_file: Path, output_file: Path):
    """
    Combina ambos archivos en output_file con cabecera estándar.
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as fout:
        fout.write("posx\tposy\th\ttype\n")
        for f in (boundary_file, fluid_file):
            if not f.exists():
                continue
            with open(f, "r", encoding="utf-8") as fin:
                lines = fin.readlines()
            start = 1 if len(lines) > 0 and any(tok.isalpha() for tok in lines[0].split()) else 0
            for line in lines[start:]:
                if line.strip():
                    fout.write(line.rstrip() + "\n")


def export_all_particles(
    output_filename: str = "all_particles.txt",
    visualize: bool = False,
    output_dir: Path = None
):
    """
    Genera archivos individuales, combina en uno solo y retorna las listas de partículas.

    Retorna:
        boundary_parts, fluid_parts: listas de dicts con keys 'id', 'position', 'h', 'type'
    """
    if output_dir is None:
        output_dir = Path(__file__).resolve().parents[1] / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    boundary_fname = "boundary_particles.txt"
    fluid_fname = "fluid_particles.txt"
    boundary_path = output_dir / boundary_fname
    fluid_path = output_dir / fluid_fname
    output_path = output_dir / output_filename

    # Exportadores individuales
    export_boundary_particles(output_filename=boundary_fname, visualize=False, output_dir=output_dir)
    export_fluid_particles(output_filename=fluid_fname, visualize=False, output_dir=output_dir)

    # Combinar archivos
    _write_combined_file(boundary_path, fluid_path, output_path)
    print(f"[✓] Archivo combinado exportado en: {output_path}")

    # Parsear archivos a memoria
    boundary_parts = _parse_particle_file(boundary_path)
    fluid_parts = _parse_particle_file(fluid_path)

    # Visualización opcional
    if visualize:
        try:
            if boundary_parts:
                visualize_boundary(boundary_parts, show=False)
            if fluid_parts:
                import numpy as np
                pts = np.array([p["position"] for p in fluid_parts])
                visualize_fluid(pts, show=True)
        except Exception as e:
            print(f"[warning] Error en visualización conjunta: {e}")

    return boundary_parts, fluid_parts
