# neighbors/testNeighbors.py
import random
import linked_list.neighbors_linked_list as nll
from initialParticlesBuilder import build_particles_from_export

def test_neighbors(n_tests: int = 20, filename: str = "NN_test.output"):
    # 1. Construir partículas desde geometría (Python -> C++)
    particles = build_particles_from_export(plot=False)
    print(f"[Python] Geometría exportada con {len(particles)} partículas")

    if not particles:
        print("No se generaron partículas, abortando.")
        return

    # 2. Calcular bounding box del dominio de partículas
    xs = [p.pos[0] for p in particles]
    ys = [p.pos[1] for p in particles]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    h = particles[0].h  # asumimos h común o representativo

    # 3. Construir celdas
    cells = nll.buildGrid(xmin, xmax, ymin, ymax, h)
    print(f"[C++] Construidas {len(cells)} celdas")

    # 4. Asignar partículas a celdas y buscar vecinos
    nll.assignParticlesToCells(cells, particles, h)
    nll.findNeighbors(cells, particles, kappa=2.0)

    # 5. Test estilo antiguo → escribir a archivo
    with open(filename, "w") as f:
        for _ in range(n_tests):
            p = random.choice(particles)
            f.write(f"{p.id} {p.pos[0]} {p.pos[1]}\n")
            for nid in p.neighbors:
                pj = particles[nid]
                f.write(f"{pj.id} {pj.pos[0]} {pj.pos[1]}\n")
            f.write("\n")

    print(f"[Test] Vecinos exportados a {filename}")

if __name__ == "__main__":
    test_neighbors()
