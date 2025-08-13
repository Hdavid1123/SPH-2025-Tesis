# initial_conditions/fluid/export.py

from pathlib import Path
from .builder import FluidBuilder
from .particleizer import FluidParticleizer
from .visualizer import visualize_fluid
from .stats import save_stats

def export_fluid_particles(output_filename: str = "fluid_particles.txt", visualize: bool = False):
    # 1. Construir puntos del fluido
    builder = FluidBuilder()
    points = builder.build()  # Ya incluye chequeo de fronteras si lo configuraste

    # 2. Convertir puntos en partículas SPH
    particleizer = FluidParticleizer()
    particles = particleizer.generate(points)

    # 3. Ruta de salida en outputs/
    output_dir = Path(__file__).resolve().parents[1] / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / output_filename

    # 4. Guardar como TXT (igual que boundaries/export.py)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("posx\tposy\th\ttype\n")
        for p in particles:
            x, y = p["position"]
            h = p["h"]
            ptype = p["type"]
            f.write(f"{x:.6f}\t{y:.6f}\t{h:.6f}\t{ptype}\n")

    print(f"[✓] Archivo de fluido exportado en: {output_path}")

    # 5. Guardar estadísticas
    save_stats(points, output_dir)

    # 6. Visualizar si se solicita
    if visualize:
        visualize_fluid(points, show=True)
