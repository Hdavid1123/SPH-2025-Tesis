import matplotlib.pyplot as plt
from boundaries.geometry_build import construir_geometria_desde_parametros
import numpy as np

def graficar_geometria(point_size=1.5, figsize=(6, 6)):
    lados, lineas_extra = construir_geometria_desde_parametros()

    colores_lados = {
        "AB": "r",
        "BC": "g",
        "CD": "b",
        "DA": "m"
    }

    plt.figure(figsize=figsize)

    puntos_borde = []

    # Dibujar lados del trapecio
    for nombre_lado, puntos in lados.items():
        x, y = puntos[:, 0], puntos[:, 1]
        color = colores_lados.get(nombre_lado, "k")
        plt.scatter(x, y, c=color, label=f"Lado {nombre_lado}", s=point_size)
        puntos_borde.extend(puntos)  # Recolectar puntos del lado

    # Dibujar líneas adicionales
    for i, linea in enumerate(lineas_extra):
        x, y = linea[:, 0], linea[:, 1]
        plt.scatter(x, y, c='k', marker="x", label=f"Línea extra {i+1}", s=point_size)
        puntos_borde.extend(linea)  # Recolectar puntos de la línea

    plt.gca().set_aspect('equal')
    plt.grid(True)
    plt.title("Geometría generada")
    plt.legend()
    plt.xlim(-0.6, 0.6)
    plt.ylim(-0.6, 0.6)
    plt.show()

    return np.array(puntos_borde)