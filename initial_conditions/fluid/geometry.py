import numpy as np
from matplotlib.path import Path

def sample_fluid_region(config: dict) -> np.ndarray:
    """Genera puntos dentro de un cuadrilátero definido por vértices."""
    v = config["vertices"]
    vertices = [np.array(v["A"]), np.array(v["B"]),
                np.array(v["C"]), np.array(v["D"])]

    xs, ys = zip(*vertices)
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    if config.get("flag_N", "False") == "True":
        nx = config["nx"]
        ny = config["ny"]
        x_vals = np.linspace(min_x, max_x, nx, endpoint=True)
        y_vals = np.linspace(min_y, max_y, ny, endpoint=True)
    else:
        spacing = config["espaciado"]
        x_vals = np.arange(min_x, max_x + spacing, spacing)
        y_vals = np.arange(min_y, max_y + spacing, spacing)

    xx, yy = np.meshgrid(x_vals, y_vals)
    puntos = np.vstack((xx.flatten(), yy.flatten())).T

    poligono = Path(vertices)
    return puntos[poligono.contains_points(puntos)]
