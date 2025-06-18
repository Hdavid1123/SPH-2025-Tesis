import numpy as np
from scipy.spatial import cKDTree

def eliminar_solapamientos(p_fluid, p_border, distancia_minima):
    if len(p_border) == 0:
        return p_fluid

    tree_border = cKDTree(p_border)
    distancias, _ = tree_border.query(p_fluid, k=1)
    mascara = distancias > distancia_minima
    return p_fluid[mascara]