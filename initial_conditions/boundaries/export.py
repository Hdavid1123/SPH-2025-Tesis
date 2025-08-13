# initial_conditions/boundaries/export.py
from pathlib import Path
from .builder import BoundaryBuilder
from .visualizer import visualize_boundary

def export_boundary_particles(output_filename: str = "boundary_particles.txt",
                              visualize: bool = False,
                              output_dir: Path = None):
    builder = BoundaryBuilder()
    particles = builder.build()

    # Filtrar partículas válidas
    valid_particles = []
    for p in particles:
        if not isinstance(p, dict):
            continue
        if "position" not in p or p["position"] is None:
            continue
        if len(p["position"]) != 2:
            continue
        valid_particles.append(p)

    # Ruta de salida configurable
    if output_dir is None:
        output_dir = Path(__file__).resolve().parents[1] / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / output_filename

    # Guardar archivo
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("posx\tposy\th\ttype\n")
        for p in valid_particles:
            x, y = p["position"]
            h = p["h"]
            ptype = p["type"]
            f.write(f"{x:.6f}\t{y:.6f}\t{h:.6f}\t{ptype}\n")

    print(f"[✓] Archivo exportado en: {output_path}")

    if visualize:
        visualize_boundary(valid_particles, show=True)
