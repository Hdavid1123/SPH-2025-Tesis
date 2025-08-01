import matplotlib.pyplot as plt
import numpy as np

from boundaries.geometry_build import construir_geometria_desde_parametros
from fluid.geometry_const import construir_fluido

def visualizar_borde_y_fluido(point_size=4, figsize=(8, 8)):
    # Construir geometría de frontera (lados y líneas extra)
    lados, lineas_extra = construir_geometria_desde_parametros()

    # Combinar todos los puntos de frontera
    puntos_borde = np.concatenate(list(lados.values()) + lineas_extra)

    # Construir partículas de fluido, evitando solapamientos
    puntos_fluido = construir_fluido(puntos_frontera=puntos_borde)

    # Graficar ambos
    plt.figure(figsize=figsize)
    plt.scatter(puntos_borde[:, 0], puntos_borde[:, 1], s=point_size, c='black', label='Borde')
    plt.scatter(puntos_fluido[:, 0], puntos_fluido[:, 1], s=point_size, c='blue', label='Fluido')
    plt.axis("equal")
    plt.legend()
    plt.title("Frontera y región de fluido")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
