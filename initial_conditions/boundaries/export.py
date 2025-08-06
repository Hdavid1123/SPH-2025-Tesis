# initial_conditions/boundaries/export.py

from pathlib import Path
from .builder import BoundaryBuilder
from .visualizer import visualize_boundary


def export_boundary_particles(output_filename: str = "boundary_particles.txt", visualize: bool = False):
    builder = BoundaryBuilder()
    particles = builder.build()  # Usa el resolution que viene del JSON

    # Ruta de salida: dentro de outputs/
    output_path = Path(__file__).resolve().parents[1] / "outputs" / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)  # Crea outputs/ si no existe

    # Escribir archivo de texto
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("posx\tposy\th\ttype\n")
        for p in particles:
            x, y = p["position"]
            h = p["h"]
            ptype = p["type"]
            f.write(f"{x:.6f}\t{y:.6f}\t{h:.6f}\t{ptype}\n")

    print(f"[✓] Archivo exportado en: {output_path}")

    # Visualizar si se solicita
    if visualize:
        visualize_boundary(particles, show=True)