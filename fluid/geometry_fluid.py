import numpy as np
from matplotlib.path import Path

def generar_particulas_fluidas(config):

    # Leer y ordenar los vértices
    v = config["vertices"]
    vertices = [np.array(v["A"]), np.array(v["B"]),
                np.array(v["C"]), np.array(v["D"])]

    # Bounding box
    xs, ys = zip(*vertices)
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    if config["flag_N"] == "True":
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

    # Filtrar puntos que estén dentro del polígono
    poligono = Path(vertices)
    puntos_filtrados = puntos[poligono.contains_points(puntos)]

    return puntos_filtrados

