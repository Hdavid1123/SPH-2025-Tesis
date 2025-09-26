# main.py
import sys
from pathlib import Path

# --- Ajustar rutas ---
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# --- Imports internos ---
from interface_pyCpp.initialParticlesBuilder import build_particles_from_export
from algoritms.neighbors import neighbors_linked_list as nll
#from algoritms.testNeighbors import test_neighbors


def main():
    print("=== Pipeline SPH Vecinos (Python + C++) ===")

    # 1. Construir partículas (Python -> C++)
    particles = build_particles_from_export(plot=False)
    print(f"[Pipeline] Construidas {len(particles)} partículas en C++")

    if not particles:
        print("[Error] No se generaron partículas, abortando.")
        return

    # 2. Calcular bounding box del dominio de partículas
    xs = [p.pos[0] for p in particles]
    ys = [p.pos[1] for p in particles]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    h = particles[0].h  # asumimos h representativo

    # 3. Construir celdas
    cells = nll.buildGrid(xmin, xmax, ymin, ymax, h)
    print(f"[Pipeline] Construidas {len(cells)} celdas en C++")

    # 4. Asignar partículas a celdas
    nll.assignParticlesToCells(cells, particles, h)
    print("[Pipeline] Partículas asignadas a celdas")

    # 5. Calcular vecinos
    nll.findNeighbors(cells, particles, kappa=2.0)
    print("[Pipeline] Vecinos calculados")

    # 6. Ejecutar test de vecinos
    #test_neighbors(n_tests=20, filename="NN_test.output")
    #print("[Pipeline] Test de vecinos completado")


if __name__ == "__main__":
    main()
