# initial_conditions/fluid/export.py
from pathlib import Path
from .builder import FluidBuilder
from .particleizer import FluidParticleizer
from .visualizer import visualize_fluid

def export_fluid_particles(output_filename: str = "fluid_particles.txt", visualize: bool = False, output_dir: Path = None):
    builder = FluidBuilder()
    points = builder.build()

    particleizer = FluidParticleizer()
    particles = particleizer.generate(points)

    if output_dir is None:
        output_dir = Path(__file__).resolve().parents[1] / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / output_filename

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("posx\tposy\th\ttype\n")
        for p in particles:
            x, y = p["position"]
            h = p["h"]
            ptype = p["type"]
            f.write(f"{x:.6f}\t{y:.6f}\t{h:.6f}\t{ptype}\n")

    print(f"[✓] Archivo de fluido exportado en: {output_path}")

    if visualize:
        visualize_fluid(points, show=True)
