# initial_conditions/export_all.py

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from boundaries.builder import BoundaryBuilder
from boundaries.visualizer import visualize_boundary
from fluid.builder import FluidBuilder
from fluid.particleizer import FluidParticleizer
from fluid.visualizer import visualize_fluid


def export_all_particles(output_filename: str = "all_particles.txt", visualize: bool = False):
    """
    Exporta partículas de frontera y fluido a un mismo archivo .txt,
    filtrando el fluido para evitar solapamientos con las fronteras
    y graficando ambos en el mismo eje si visualize=True.
    """

    # 1. Construir partículas de frontera
    boundary_builder = BoundaryBuilder()
    boundary_particles = boundary_builder.build()

    # Extraer posiciones de frontera como array para filtrado
    border_points = np.array([p["position"] for p in boundary_particles])

    # 2. Construir puntos del fluido evitando solapamientos
    fluid_builder = FluidBuilder()
    points_fluid = fluid_builder.build(border_points=border_points)

    # 3. Convertir puntos de fluido a partículas SPH
    fluid_particleizer = FluidParticleizer()
    fluid_particles = fluid_particleizer.generate(points_fluid, ptype=0, h=0.01)

    # 4. Ruta de salida
    output_path = Path(__file__).resolve().parents[0] / "outputs" / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 5. Guardar todo en un solo archivo
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("posx\tposy\th\ttype\n")
        for p in boundary_particles + fluid_particles:
            x, y = p["position"]
            h = p["h"]
            ptype = p["type"]
            f.write(f"{x:.6f}\t{y:.6f}\t{h:.6f}\t{ptype}\n")

    print(f"[✓] Archivo combinado exportado en: {output_path}")

    # 6. Visualización conjunta
    if visualize:
        fig, ax = plt.subplots()
        visualize_boundary(boundary_particles, ax=ax, show=False)
        visualize_fluid(points_fluid, ax=ax, show=False)

        ax.set_title("Partículas de frontera y fluido")
        ax.set_aspect('equal', 'box')
        plt.show()
