# initial_conditions/summary.py

import numpy as np
import pandas as pd
from pathlib import Path
import json


def count_particles_by_axis(points: np.ndarray, tol: float = 1e-8):
    """
    Cuenta partículas por columnas (X) y filas (Y) con tolerancia para evitar errores de flotante.
    """
    xs = np.round(points[:, 0] / tol) * tol
    ys = np.round(points[:, 1] / tol) * tol

    unique_x = np.unique(xs)
    col_counts = [{"Col": i, "Num": np.sum(xs == x)}
                  for i, x in enumerate(sorted(unique_x), start=1)]

    unique_y = np.unique(ys)
    row_counts = [{"Fil": i, "Num": np.sum(ys == y)}
                  for i, y in enumerate(sorted(unique_y, reverse=True), start=1)]

    return pd.DataFrame(col_counts), pd.DataFrame(row_counts)


def generate_summary(boundary_data: dict,
                     fluid_data: dict,
                     params_boundary: dict,
                     params_fluid: dict,
                     output_path: Path):
    """
    Genera un archivo de resumen en formato TXT y JSON con datos de frontera, fluido y parámetros.
    """

    summary_lines = []
    summary_lines.append("=== Resumen Condiciones Iniciales ===\n")

    # ===== FRONTERA =====
    summary_lines.append("[FRONTERA]")
    total_boundary = len(boundary_data["particles"])
    summary_lines.append(f"Total partículas: {total_boundary}")
    summary_lines.append(f"Espaciado: {boundary_data.get('spacing', 'N/A')} m")
    summary_lines.append(f"Secciones: {len(boundary_data.get('sections', []))}")

    # Secciones
    summary_lines.append("Posiciones de secciones:")
    for sec in boundary_data.get("sections", []):
        summary_lines.append(
            f"  {sec['name']}: inicio {sec['start']} → fin {sec['end']} "
            f"({sec['num_particles']} partículas)"
        )

    # Agujeros
    summary_lines.append("\nAgujeros:")
    if boundary_data.get("holes"):
        for hole in boundary_data["holes"]:
            summary_lines.append(
                f"  - {hole['section']}: inicio {hole['start']} → fin {hole['end']}, "
                f"eliminadas: {hole['removed']}"
            )
    else:
        summary_lines.append("  (no se definieron agujeros)")

    summary_lines.append("")

    # ===== FLUIDO =====
    summary_lines.append("[FLUIDO]")
    total_fluid = len(fluid_data["particles"])
    summary_lines.append(f"Total partículas: {total_fluid}")
    summary_lines.append(f"Área: {fluid_data.get('area', 'N/A')} m²")
    summary_lines.append(f"h: {fluid_data.get('h', 'N/A')} m")
    summary_lines.append(f"Posición inicial: {fluid_data.get('start_pos', 'N/A')}")
    summary_lines.append(f"Posición final: {fluid_data.get('end_pos', 'N/A')}")
    summary_lines.append(f"Vértices: {fluid_data.get('vertices', 'N/A')}")

    # Conteo por filas y columnas
    df_cols, df_rows = count_particles_by_axis(np.array(fluid_data["particles"]))
    summary_lines.append("\nPartículas por columna:")
    summary_lines.append(df_cols.to_string(index=False))
    summary_lines.append("\nPartículas por fila:")
    summary_lines.append(df_rows.to_string(index=False))
    summary_lines.append("")

    # ===== PARÁMETROS =====
    summary_lines.append("[PARÁMETROS]")
    summary_lines.append("boundary_conditions.json (compacto):")
    summary_lines.append(json.dumps(params_boundary, indent=2, ensure_ascii=False))
    summary_lines.append("\nfluid_region.json (compacto):")
    summary_lines.append(json.dumps(params_fluid, indent=2, ensure_ascii=False))

    # Guardar archivo TXT
    summary_path = output_path / "summary.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines))

    # Guardar archivo JSON
    summary_json = {
        "boundary": boundary_data,
        "fluid": {
            **fluid_data,
            "particles_by_col": df_cols.to_dict(orient="records"),
            "particles_by_row": df_rows.to_dict(orient="records")
        },
        "parameters": {
            "boundary_conditions": params_boundary,
            "fluid_region": params_fluid
        }
    }
    json_path = output_path / "summary.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary_json, f, indent=2, ensure_ascii=False)

    print(f"[✓] Resumen TXT guardado en: {summary_path}")
    print(f"[✓] Resumen JSON guardado en: {json_path}")

def save_compact_summary(boundary_data, fluid_data, params_boundary, params_fluid, output_path: Path):
    """
    Guarda un archivo JSON compacto con los parámetros esenciales y métricas clave.
    """
    compact = {
        "boundary": {
            "total_particles": len(boundary_data["particles"]),
            "spacing": boundary_data.get("spacing"),
            "sections": boundary_data.get("sections", []),
            "holes": boundary_data.get("holes", [])
        },
        "fluid": {
            "total_particles": len(fluid_data["particles"]),
            "area": fluid_data.get("area"),
            "h": fluid_data.get("h"),
            "start_pos": fluid_data.get("start_pos"),
            "end_pos": fluid_data.get("end_pos"),
            "vertices": fluid_data.get("vertices")
        },
        "parameters": {
            "boundary_conditions": params_boundary,
            "fluid_region": params_fluid
        }
    }

    path = output_path / "params_summary.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(compact, f, indent=2, ensure_ascii=False)
    print(f"[✓] Resumen compacto de parámetros guardado en: {path}")
