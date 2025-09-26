# initialParticlesBuilder.py
import sys
from pathlib import Path

# Agrega el root del proyecto al path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from . import initial_particles_builder as ipb
from initial_conditions.export_all import export_all_particles

def build_particles_from_export(plot: bool = False):
    """
    Obtiene el array de partículas ya construido por export_all_particles
    y lo pasa a C++ sin tocar el .txt.
    """
    _, data_for_cpp = export_all_particles(visualize=plot)
    particles_cpp = ipb.inicializar_particulas(data_for_cpp)
    return particles_cpp

if __name__ == "__main__":
    particles_cpp = build_particles_from_export(plot=False)
    print(f"[C++] Se recibieron {len(particles_cpp)} partículas")
    if particles_cpp:
        p0 = particles_cpp[0]
        print("Ejemplo partícula desde C++:")
        print(f"  id   = {p0.id}")
        print(f"  pos  = {p0.pos}")
        print(f"  mass = {p0.mass}")
        print(f"  h    = {p0.h}")
        print(f"  type = {p0.type}")
