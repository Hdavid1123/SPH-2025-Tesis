import matplotlib.pyplot as plt
from typing import List, Tuple

Point = Tuple[float, float]
Segment = List[Point]


def visualize_boundary(particles: List[dict],
                       show: bool = True,
                       save_path: str = None,
                       ax: plt.Axes = None) -> plt.Axes:
    """
    Dibuja la nube de partículas SPH como representación de la frontera.

    Args:
        particles: lista de partículas, cada una con campos incluyendo 'position'.
        show: si True muestra el plot al final (plt.show()).
        save_path: si se especifica, guarda la imagen en esa ruta.
        ax: eje existente donde dibujar (opcional).

    Returns:
        plt.Axes: el eje donde se dibujó.
    """
    own_ax = ax is None
    if own_ax:
        fig, ax = plt.subplots()

    xs = [p["position"][0] for p in particles]
    ys = [p["position"][1] for p in particles]

    ax.plot(xs, ys, 'ko', markersize=2)

    #ax.set_xlim(-0.6, 0.6)
    #ax.set_ylim(-0.6, 0.6)

    ax.set_aspect('equal', 'box')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Frontera SPH')

    if save_path:
        plt.savefig(save_path, dpi=150)
    elif show and own_ax:
        plt.show()

    return ax
    return ax